"""Planner proposals and deterministic checks. Ranking never grants authorization."""
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field


class Action(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: str = Field(min_length=1)
    goal: str = Field(min_length=1)
    finding_ids: list[str] = Field(min_length=1)
    depends_on: list[str]
    action_type: Literal["investigate", "characterization_test", "fix_defect", "refactor", "defer"]
    behavior_impact: Literal["preserve", "intentional_change", "uncertain"]
    evidence_strength: Literal["observed", "tool_verified", "hypothesis"]
    risk: Literal["low", "medium", "high"]
    risk_reason: str = Field(min_length=1)
    impact: Literal["low", "medium", "high"]
    proposed_readiness: Literal["ready", "prerequisite_needed", "human_direction_needed"]
    rationale: str = Field(min_length=1)
    acceptance_checks: list[Literal["behavior_tests", "security_regression", "lint", "operation_counts", "benchmarks", "human_review"]] = Field(min_length=1)


class Conflict(BaseModel):
    model_config = ConfigDict(extra="forbid")
    summary: str = Field(min_length=1)
    affected_action_ids: list[str] = Field(min_length=1)


class Plan(BaseModel):
    model_config = ConfigDict(extra="forbid")
    version: int = Field(ge=1)
    synthesis: str = Field(min_length=1)
    conflicts: list[Conflict]
    actions: list[Action] = Field(min_length=1, max_length=12)


def validate_plan(plan: Plan, finding_ids: set[str], *, tool_verified_ids=frozenset()):
    by_id = {a.id: a for a in plan.actions}
    if len(by_id) != len(plan.actions):
        raise ValueError("Duplicate action ID")
    for conflict in plan.conflicts:
        if not set(conflict.affected_action_ids) <= by_id.keys():
            raise ValueError("Unknown conflict action")
    covered = set()
    for action in plan.actions:
        if not set(action.finding_ids) <= finding_ids:
            raise ValueError("Unknown finding reference")
        covered.update(action.finding_ids)
        if len(set(action.depends_on)) != len(action.depends_on):
            raise ValueError("Duplicate prerequisite")
        if not set(action.depends_on) <= by_id.keys():
            raise ValueError("Unknown prerequisite")
        if action.evidence_strength == "tool_verified" and not set(action.finding_ids) <= tool_verified_ids:
            raise ValueError("Tool evidence not available")
        if action.action_type in {"fix_defect", "refactor"} and "behavior_tests" not in action.acceptance_checks:
            raise ValueError("Code change requires behavioral acceptance")
    if covered != finding_ids:
        raise ValueError("Every finding requires a disposition, including deferral")
    visited, active = set(), set()

    def visit(action_id):
        if action_id in active:
            raise ValueError("Dependency cycle")
        if action_id in visited:
            return
        active.add(action_id)
        for parent in by_id[action_id].depends_on:
            visit(parent)
        active.remove(action_id)
        visited.add(action_id)

    for action_id in by_id:
        visit(action_id)


def classify_and_rank(plan: Plan, finding_ids: set[str], *, passed=frozenset(), directed=frozenset()):
    """passed/directed come from trusted coordinator state, never model output.

    Directed means a human resolved an action's behavior question, not permission
    to apply a patch. Exact-patch authorization remains a separate required gate.
    """
    validate_plan(plan, finding_ids)
    by_id = {a.id: a for a in plan.actions}
    if not set(passed) <= by_id.keys() or not set(directed) <= by_id.keys():
        raise ValueError("Unknown coordinator action state")

    def ancestors(action):
        result = set(action.depends_on)
        for parent in action.depends_on:
            result.update(ancestors(by_id[parent]))
        return result

    rows = []
    for action in plan.actions:
        reasons = []
        parents = ancestors(action)
        if not parents <= set(passed):
            reasons.append("prerequisites_not_verified")
        if (action.behavior_impact in {"uncertain", "intentional_change"} or
                action.proposed_readiness == "human_direction_needed") and action.id not in directed:
            reasons.append("human_direction_required")
        if action.proposed_readiness == "prerequisite_needed" and not parents:
            reasons.append("prerequisite_unspecified")
        if action.action_type in {"fix_defect", "refactor"}:
            test_parents = {p for p in parents if by_id[p].action_type == "characterization_test"}
            if not test_parents or not test_parents <= set(passed):
                reasons.append("characterization_required")
        if any(set(c.affected_action_ids) & (parents | {action.id}) for c in plan.conflicts):
            reasons.append("unresolved_plan_conflict")
        if action.action_type == "defer":
            reasons.append("deferred")
        if action.id in passed:
            reasons.append("already_verified")
        # Proposal-derived ranking is advisory and uses no confidence score.
        inputs = {"impact": {"low": 1, "medium": 2, "high": 3}[action.impact] * 3,
                  "evidence": {"hypothesis": 0, "observed": 1, "tool_verified": 2}[action.evidence_strength],
                  "prerequisite_value": sum(action.id in ancestors(other) for other in plan.actions),
                  "risk_penalty": {"low": 0, "medium": -1, "high": -2}[action.risk]}
        rows.append({"action_id": action.id, "ready_for_proposal": not reasons,
                     "blockers": reasons, "score_inputs": inputs, "score": sum(inputs.values()),
                     "approval_required": True, "execution_authorized": False})
    return sorted(rows, key=lambda r: (not r["ready_for_proposal"], -r["score"], r["action_id"]))
