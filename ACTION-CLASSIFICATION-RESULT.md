# Action classification and synthesis — 30 October 2026

Implemented in the bounded planner prototype. Classification is part of one
synthesis-agent response, not an additional classifier call. Model proposals
are validated and ranked by application rules; nothing here grants execution.

## Live result

Run `plan-20261030-2` used one Gemini 3.8 Flash synthesis call over the saved
four-reviewer artifact, explicitly labeled `replay_of_live_review`. The reviewers
were not rerun. The complete plan covered all five findings with five actions:

| Action | Classification | Current disposition |
|---|---|---|
| Characterize collection behavior | Test, preserve behavior | Eligible for patch proposal |
| Characterize legitimate query behavior | Test, preserve behavior | Eligible for patch proposal |
| Parameterize SQL query | Defect fix, intentional change | Tests and human direction required; driver contract unresolved |
| Optimize collection lookup | Refactor, preserve behavior proposed | Tests required; input-type contract unresolved |
| Rename public identifiers | Defer | Public API compatibility and conventions need clarification |

The SQL fix received a higher advisory score (9) than the collection test (8),
but remained blocked. This demonstrates the distinction between priority and
readiness. Both test steps are merely eligible for proposal: test patches still
need their own exact-patch authorization. All five actions have
`execution_authorized=false`.

Every action includes type, behavior impact, evidence strength, risk and reason,
impact, proposed readiness, finding references, dependencies and typed acceptance
checks. Application code checks coverage, IDs, cycles, source references and
unsupported tool-verification claims, and calculates explicit blockers and score
inputs. Classification and priority remain advisory, not calibrated success
probabilities. No model confidence score is used.

## Verification

Eight offline rule tests passed, covering priority versus prerequisites,
characterization requirements, human direction, scoped conflict propagation,
cycles and invalid references, unsupported tool evidence, and deferral. No
classified action can authorize execution through this component.

LangGraph persisted the complete plan at a review interrupt. A separate process
recovered the same digest without a model call:

    0bcf7650bca95699c29f4fc2d2d9176668f0f7499e54b4ce8d96adaf98026151

Commands verified locally:

    .\.venv\Scripts\python.exe -m unittest test_action_planning -v
    .\.venv\Scripts\python.exe spike_plan.py inspect --run plan-20261030-2

Local evidence: `artifacts/plan-spike/result.json` and SQLite checkpoint. The
earlier `plan-20261030-1` exposed overly broad conflict blocking; after an explicit
schema/rule revision, the second live call verified scoped conflict propagation.
Each attempt used one synthesis call; these are development runs, not evaluation
scores. The SQLite records retain both runs; the JSON export is the latest run.

## Limits and next step

This is a synthesis/classification prototype over replayed synthetic evidence,
not an integrated intake-to-execution application. Passed-step and direction
inputs are trusted-state interfaces awaiting the real coordinator and approval
ledger. Conflict resolution requires a revised plan; pending approvals must be
invalidated then. No test edits or production edits have been applied. Exact
patch generation/approval and container verification remain the next slice.
