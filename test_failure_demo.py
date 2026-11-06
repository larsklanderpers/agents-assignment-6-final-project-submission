"""Policy checks only; never approves or runs the real negative-case candidate."""
import unittest
from unittest.mock import patch

import failure_demo as demo
from action_planning import classify_and_rank


class FailureDemoRules(unittest.TestCase):
    def test_negative_case_needs_direction_and_cannot_unblock_descendant(self):
        plan=demo.initial_plan('verified-characterization')
        no_direction={r['action_id']:r for r in classify_and_rank(plan,demo.FINDINGS,passed={'verified-characterization'})}
        self.assertFalse(no_direction[demo.FAULT]['ready_for_proposal'])
        directed={r['action_id']:r for r in classify_and_rank(plan,demo.FINDINGS,
            passed={'verified-characterization'},directed={demo.FAULT})}
        self.assertTrue(directed[demo.FAULT]['ready_for_proposal'])
        self.assertFalse(directed[demo.FOLLOW]['ready_for_proposal'])
        self.assertFalse(directed[demo.FAULT]['execution_authorized'])

    def test_preparation_stops_without_verified_snapshot(self):
        with patch.object(demo.opt,'validate',side_effect=ValueError('Missing verified prerequisite')):
            with self.assertRaises(ValueError):demo.prepare()

    def test_fault_proposal_changes_only_lookup_function(self):
        original=b'def find_users(connection, name):\n    return name\n\ndef Common_Items(list, other):\n    return list\n'
        proposed=demo.faulty_source(original)
        demo.opt.validate_source(original,proposed)
        self.assertTrue(proposed.startswith(original.split(b'def Common_Items')[0]))
        self.assertNotEqual(demo.policy('fault')['bootstrap_sha256'],demo.policy('repair')['bootstrap_sha256'])


if __name__=='__main__':unittest.main()
