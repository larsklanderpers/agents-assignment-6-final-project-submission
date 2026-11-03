import unittest

from action_planning import Action, Plan, classify_and_rank, validate_plan


def action(id="test", **changes):
    values = dict(id=id, goal="Characterize behavior", finding_ids=["f1"], depends_on=[],
                  action_type="characterization_test", behavior_impact="preserve",
                  evidence_strength="observed", risk="low", risk_reason="Small test proposal",
                  impact="medium", proposed_readiness="ready", rationale="Establish contract",
                  acceptance_checks=["behavior_tests"])
    values.update(changes)
    return Action(**values)


def plan(*actions, conflicts=None):
    return Plan(version=1, synthesis="Test synthesis", conflicts=conflicts or [], actions=list(actions))


class PlanningRules(unittest.TestCase):
    def test_high_priority_cannot_bypass_prerequisite_or_authorize_execution(self):
        p = plan(action(), action("fix", depends_on=["test"], action_type="refactor", impact="high"))
        rows = {r["action_id"]: r for r in classify_and_rank(p, {"f1"})}
        self.assertTrue(rows["test"]["ready_for_proposal"])
        self.assertFalse(rows["fix"]["ready_for_proposal"])
        self.assertIn("prerequisites_not_verified", rows["fix"]["blockers"])
        completed = {r["action_id"]: r for r in classify_and_rank(p, {"f1"}, passed={"test"})}
        self.assertTrue(completed["fix"]["ready_for_proposal"])
        self.assertTrue(completed["fix"]["approval_required"])
        self.assertFalse(completed["fix"]["execution_authorized"])

    def test_intentional_change_requires_human_direction_even_after_tests(self):
        p = plan(action(), action("fix", depends_on=["test"], action_type="fix_defect",
                                  behavior_impact="intentional_change"))
        rows = classify_and_rank(p, {"f1"}, passed={"test"})
        self.assertFalse(next(r for r in rows if r["action_id"] == "fix")["ready_for_proposal"])
        rows = classify_and_rank(p, {"f1"}, passed={"test"}, directed={"fix"})
        fix = next(r for r in rows if r["action_id"] == "fix")
        self.assertTrue(fix["ready_for_proposal"])
        self.assertFalse(fix["execution_authorized"])

    def test_uncertain_behavior_and_conflicts_block(self):
        for p in [plan(action(behavior_impact="uncertain")), plan(action(), conflicts=[
                {"summary": "Contract disputed", "affected_action_ids": ["test"]}])]:
            self.assertFalse(classify_and_rank(p, {"f1"})[0]["ready_for_proposal"])

    def test_conflict_blocks_affected_actions_and_descendants_only(self):
        p = plan(action(), action("fix", depends_on=["test"], action_type="refactor"),
                 action("later", depends_on=["fix"], action_type="refactor"), conflicts=[
                     {"summary": "Hashability unknown", "affected_action_ids": ["fix"]}])
        rows = {r["action_id"]: r for r in classify_and_rank(p, {"f1"})}
        self.assertTrue(rows["test"]["ready_for_proposal"])
        self.assertIn("unresolved_plan_conflict", rows["fix"]["blockers"])
        self.assertIn("unresolved_plan_conflict", rows["later"]["blockers"])

    def test_unverified_tool_claim_rejected(self):
        with self.assertRaises(ValueError):
            validate_plan(plan(action(evidence_strength="tool_verified")), {"f1"})

    def test_cycles_unknown_references_and_omissions_rejected(self):
        bad = [plan(action(depends_on=["test"])), plan(action(depends_on=["missing"])),
               plan(action(finding_ids=["invented"])), plan(action(), action())]
        for p in bad:
            with self.subTest(p=p), self.assertRaises(ValueError):
                validate_plan(p, {"f1"})
        with self.assertRaises(ValueError):
            validate_plan(plan(action()), {"f1", "f2"})

    def test_readiness_claim_cannot_substitute_for_characterization(self):
        rows = classify_and_rank(plan(action(action_type="refactor")), {"f1"})
        self.assertIn("characterization_required", rows[0]["blockers"])
        with self.assertRaises(ValueError):
            validate_plan(plan(action(action_type="refactor", acceptance_checks=["lint"])), {"f1"})

    def test_deferral_and_unexplained_prerequisite_cannot_be_ready(self):
        for a in [action(action_type="defer"), action(proposed_readiness="prerequisite_needed")]:
            self.assertFalse(classify_and_rank(plan(a), {"f1"})[0]["ready_for_proposal"])


if __name__ == "__main__":
    unittest.main()
