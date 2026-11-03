import asyncio
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from hardening_review import validate_findings, ROLES
from evaluation.end_to_end import Plan, PlannedStep, Proposal, validate_plan, validate_proposal, execute_simulated, evaluate_case


def case():
    return {'id': 'fixture', 'source_path': 'module.py', 'files': {'module.py': {'role': 'source', 'content': 'def add(a,b):\n    return a-b\n'}},
            'contracts': {'sum': 'Return the sum'}, 'hidden_tests': 'SECRET_ORACLE',
            'labels': [{'category': 'security', 'symbol': 'add'}], 'expected': 'repair'}


class HardeningTests(unittest.TestCase):
    def test_evidence_contract_filter_retains_suggestions(self):
        raw = {r: json.dumps({'agent_id': r, 'findings': [], 'limitations': []}) for r in ROLES}
        finding = {'category': 'security', 'path': 'module.py', 'line': 2, 'evidence': '    return a-b',
                   'disposition': 'defect', 'contract_id': 'sum', 'summary': 'Wrong operation', 'consequence': 'Wrong sum', 'suggested_action': 'Add'}
        raw['security'] = json.dumps({'agent_id': 'security', 'findings': [finding, finding, {**finding, 'contract_id': 'invented'}], 'limitations': []})
        raw['test_gap'] = json.dumps({'agent_id': 'test_gap', 'findings': [{**finding, 'category': 'test_gap'}], 'limitations': []})
        accepted, retained = validate_findings(raw, case()['files'], case()['contracts'])
        self.assertEqual(len(accepted), 1)
        self.assertEqual(len(retained), 3)
        finding['evidence'] = 'return a-b'
        raw['security'] = json.dumps({'agent_id': 'security', 'findings': [finding], 'limitations': []})
        with self.assertRaises(ValueError): validate_findings(raw, case()['files'], case()['contracts'])

    def test_plan_rejects_wrong_scope_and_dependencies(self):
        for step in [PlannedStep(id='repair', path='other.py', goal='fix', depends_on=['baseline'], contract_ids=['sum']),
                     PlannedStep(id='repair', path='module.py', goal='fix', depends_on=[], contract_ids=['sum'])]:
            with self.assertRaises(ValueError): validate_plan(Plan(rationale='fix', steps=[step]), case())

    def test_proposal_protects_interface_imports_and_tests(self):
        for path_name, source in [('tests/test_x.py', 'def add(a,b):\n return a+b\n'),
                                  ('module.py', 'def renamed(a,b):\n return a+b\n'),
                                  ('module.py', 'import os\ndef add(a,b):\n return a+b\n')]:
            with self.assertRaises(ValueError): validate_proposal(Proposal(path=path_name, content=source, rationale='fix'), case())

    def test_simulated_graph_preserves_parent_and_rejects_stale_grants(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = case(); before = json.dumps(c, sort_keys=True)
            plan = Plan(rationale='repair', steps=[PlannedStep(id='repair', goal='sum', path='module.py', depends_on=['baseline'], contract_ids=['sum'])])
            proposal = Proposal(path='module.py', content='def add(a,b):\n    return a+b\n', rationale='correct addition')
            patch_text = validate_proposal(proposal, c)
            with patch('evaluation.end_to_end.run_tests', return_value={'status': 'passed', 'tests': 1}):
                outcome = execute_simulated(c, plan, proposal, patch_text, Path(tmp)/'candidate', {'status': 'passed'}, 'reviewhash')
            self.assertEqual(outcome['state'], 'VERIFIED')
            self.assertEqual(json.dumps(c, sort_keys=True), before)
            self.assertIn('wrong-mode', outcome['approval_integrity_checks'])

    def test_failed_reviews_remain_failed_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            with patch('evaluation.end_to_end.run_tests', side_effect=[{'status':'passed'}, {'status':'failed'}]), \
                 patch('evaluation.end_to_end.review_files', side_effect=ValueError('bad evidence')):
                result = asyncio.run(evaluate_case(case(), Path(tmp)/'case', 1))
            self.assertFalse(result['success'])
            self.assertEqual(result['status'], 'failed')


if __name__ == '__main__': unittest.main()
