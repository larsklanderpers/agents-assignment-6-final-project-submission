# Development handoff — 2 November 2026

Current successor: [CONTINUATION-RESULT-2026-11-02.md](CONTINUATION-RESULT-2026-11-02.md). The details below remain preserved historical context.

## Active user request

User authorized **corpus evaluation and fresh-clone packaging**, with a **detailed
demonstration runbook** for a presentation on **Thursday 5 November 2026,
Australia/Sydney**. Save this handoff first because chat context is high. Continue
in a fresh chat without repeating completed design/model experiments. Finish
DEMO-RUNBOOK.md with tested commands, exact human prompts, expected results,
speaking notes, failure recovery and a measured <=10-minute rehearsal. Canvas
submission deadline remains unconfirmed; presentation date is user-provided.

## Workspace and preservation

Project: `C:\vc-personal-projects\continuing-education\agents-assignment-6-final-project-submission`

Remote: `https://github.com/larsklanderpers/agents-assignment-6-final-project-submission.git`

Branch: `implementation/first-patch`, based on design commit `4c4ca01`. Inspect
current Git status/log; substantial implementation was developed locally. Nothing
has been pushed or merged. No root AGENTS.md was found; check for new applicable
instructions. Original clean clone remains in `../capstone-git-staging`; do not
overwrite current work from it. Existing local source, .venv, .env and artifacts
were preserved when authenticated Git metadata was added.

`.env`/`.env.*` (except `.env.example`), `.venv/` and `artifacts/` are ignored.
NEVER print/export/commit secrets. Preserve ignored artifacts and workspaces:
they contain real approvals, checkpoints, model results, failed and accepted
patches, and logs. Do not delete them to obtain a fresh demo.

## Setup already done — do not ask user to repeat

- Python 3.12.14 at `.venv\Scripts\python.exe`. `requirements-spike.lock` records
  ADK 2.13.0, LangGraph 1.2.18 and SQLite checkpointer 3.1.2, among dependencies.
  A clean install from this snapshot is NOT yet verified. Venv ensurepip failed
  initially; installation succeeded with bundled Python pip's `--python` option.
- Bootstrap runtime if needed:
  `C:\Users\LARSKLANDER\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`.
- Local `.env` has Gemini key and `REVIEW_LEDGER_MODEL=gemini-3.8-flash`.
  User enabled billing; real structured-output calls succeeded. Earlier 504s do
  not prove a bad key. 3.7 API alias redirects to 3.8 per checked official docs.
- GitHub CLI 2.103.3 and Git authenticated as larsklanderpers.
  CLI: `C:\Program Files\GitHub CLI\gh.exe` if PATH is stale.
- Docker Desktop 4.97.0 / Engine 29.9.2, Linux backend; may need starting after
  shutdown. CLI: `C:\Program Files\Docker\Docker\resources\bin\docker.exe`.
- Locally available pinned image:
  `python@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f`.
- Restricted tool execution cannot reliably use Docker pipe, Git subprocesses or
  asyncio's loopback setup. Appropriate escalation for local engine/process
  access works. This is not an account setup problem. Human terminals work in
  the normal local user session.

## Architecture and implemented behavior

ADK hosts all six reasoning agents: four parallel specialists, synthesis/planner,
patch author. LangGraph owns persisted lifecycle/HITL. Independent outputs are
strictly validated, matched to agent identity and source-line evidence. Action
classification is part of synthesis, NOT a separate model call. Deterministic
rules validate references/DAG, scope conflicts and derive readiness/priority;
scores cannot grant authorization or bypass prerequisites.

Compatibility finding: ADK forwards extra=forbid's additional_properties into
a Gemini schema transport that rejects it. Provider-facing schemas omit that
field; returned JSON still passes separate strict local schemas. ParallelAgent
works under pinned ADK but emits a Workflow deprecation warning. Avoid an
unjustified framework migration just before the presentation.

User personally approved FOUR exact patches in local interactive terminals.
Do not tool-enter or simulate real approvals. Approvals bind actor, exact patch,
parent, plan, scope and policy; single use, 30-minute expiry from issuance.
Deferral has no expiry. SQLite atomically consumes approval and creates an
operation; durable lock excludes concurrent operators. Simulation mode exists
only for tests and cannot impersonate the normal endpoint.

Execution uses detached disposable Git clones and pinned Docker, exporting only
allowlisted files over stdin. No host mounts, .git, credentials, Docker socket or
network. Non-root/read-only root/dropped capabilities/no-new-privileges plus
memory, CPU, process, time, temporary-storage and log limits. Required checks
must run; zero-test baseline is no_tests, not a green suite. Failure quarantines
the workspace. Reconciliation recognizes applied bytes instead of applying
twice. This remains a bounded synthetic-corpus prototype, not certification for
arbitrary hostile repositories. No automatic merge, push or deployment.

## Verified operations — do not rerun just to confirm history

1. **Test prerequisite VERIFIED:** FIRST-APPROVED-RESULT.md.
   `artifacts/first-patch/candidate-c2a7ed975417-exec-v1/`;
   op `06282e7e8ba947be8afd68a45251da6f`.
   Seven tests passed: empties/order/duplicates/unhashables/no mutation.
   Accepted tree `3470718602111dffa871d71cd8ae7d6f1665e2cb`.
2. **Optimization VERIFIED:** OPTIMIZATION-RESULT.md.
   `artifacts/optimization/candidate/`; op `078e14ef548e49978f293f66a82d30a7`.
   Seven tests + thirteen reference checks passed. Tree
   `54b613b65bf2d39ee3b88e25d53ff4ae023afaaf`.
   2,500-integer case median 115.379 ms -> 0.620 ms, ~186x for that case only.
3. **Controlled negative case FAILED:** FAILURE-REPLANNING-RESULT.md.
   `artifacts/failure-demo/fault/`; op `8a0b2ee93b004e378682d2ec7805c293`.
   Six passes, one real nested-list TypeError from unguarded set(other); exit 1.
   Workspace quarantined. Independent branch from test-bearing parent; successful
   optimization untouched. Fault injection was in the proposed diff BEFORE
   approval, not modification of approved bytes or a fabricated tool failure.
4. **Live replanning and separate repair VERIFIED:** RECOVERY-RESULT.md.
   Actual logs fed ADK planner; demo plan 3 -> 4. Failed action deferred; repair
   starts from last verified parent. Descendant redirected to depend on repair.
   Old approval replay against new candidate rejected without extra operation.
   `artifacts/failure-demo/repair/`; op `25d22a7e90b144a3a562fbf63a0fd608`.
   Seven tests + thirteen checks passed. Tree
   `d58ca79475a8fae1511101fafe00cbed83dd7286`.
   Integer median 94.421 ms -> 0.527 ms (~179x for this case only).

Timing uses five warmups/twenty trials per version, with equivalence checks and
ranges. It is elapsed time, not operation counts or a general workload claim.
Fast path uses extra memory. Fallback preserves other input handling.

All inspected operations have matching bindings, log hashes, resulting trees and
complete LangGraph outcomes. Parent baselines are clean; failed workspace is
still quarantined. `artifacts/failure-demo/completion.json` records real trusted
passed steps: dependent follow-up is eligible for PROPOSAL, NOT authorized or
executed. That artificial follow-up need not be built before packaging/evaluation.

## Code map and verification

- spike_adapter.py / spike_persistence.py: deterministic transport and separate
  process restart fixtures; do not present these as model reviews.
- spike_live.py: real parallel reviews; original ten-line SOURCE fixture.
- action_planning.py: strict actions/plan/DAG, scoped conflicts, advisory weights
  and readiness from trusted passed-step/direction state.
- spike_plan.py: real synthesis over explicitly replayed live review evidence.
- prepare_first_patch.py: ADK author proposes tests, without applying them.
- approval_executor.py: interface, lock/ledger, sandbox, quarantine/reconciliation;
  generic callbacks now support source patches without changing first policy.
- optimization_step.py / optimization_checks.py: fresh parent reviews, plan 2,
  guarded fast path, reference comparisons and trusted timing harness.
- failure_demo.py: disclosed fault proposal, failure inspection, live replan and
  patch author, versioned plans, stale-grant rejection and repair gate.
- Existing approve-*.cmd launchers refer to FIXED historical runs. Reopening a
  completed one displays recorded outcome, NOT a new live run. Old failure gate
  is invalidated by plan 4. Preserve these records; build fresh-run support.

Passed: 8 planning tests; 12 approval/recovery tests; 2 optimization boundary
tests; 3 failure-demo policy tests; real Docker integration (9 isolation probes
plus explicit zero-test baseline); separate-process fixture restart test.
See test_*.py. Broaden/repeat when new changes justify it. Test simulations are
not evidence of human approval. Code/script results are bounded prototypes,
not the full corpus evaluation or a fresh-clone application yet.

## Next authorized work, in order

1. **Coherent rerunnable packaging/entrypoint.** Current scripts hardcode IDs,
   paths and prior artifacts. prepare_first_patch generates UUIDs while
   approval_executor.prepare references the fixed original ID. Ignored artifacts
   will be absent from fresh clone. Introduce run manifests/run-specific IDs and
   a fresh demo path without deleting history. A read-only status/evidence
   command and a new-run command will help. Preserve invariants and measured
   history; avoid unnecessary new frameworks/features.
2. **Corpus evaluation** from EVALUATION.md: six development cases, six held-out
   variants, four clean controls, original labels/corrected variants outside
   agent snapshots. Freeze labels BEFORE evaluation. Report actual category
   metrics, denominators, all repeats/failures, behavior/test usefulness/approval
   integrity/recovery, cost/latency. Compare single-reviewer and non-replanning
   baselines if feasible; disclose missing coverage. Never call one fixture's
   benchmark the corpus result. Evaluation actors must be explicitly simulated.
3. **Fresh-clone proof:** locked install, config/credential checks, Docker image
   preparation, run commands, missing-service handling, instructor access.
   GitHub PR intake and broader corpus integration remain open despite CLI
   authentication. Distinguish GitHub/Git integration from connector doc fetching.
4. **Detailed DEMO-RUNBOOK.md** for Thursday: exact tested steps/prompts/outputs,
   timed speaking notes, live-vs-saved labels, screen/evidence locations, failure
   and recovery route, offline fallback, recording and <=10-minute rehearsal.
   Prioritize reliability and explainability; student must explain every line.
5. Update README/architecture/reflection/delivery mapping to observed results;
   reconcile chronological status contradictions. Typesetting/page-count check
   and recording remain. Canvas date, page-count interpretation, two-track
   handling and instructor permissions remain unconfirmed. Do not ask user to
   repeat completed billing/login/Docker setup.

Read CAPSTONE-REQUIREMENTS.md, EVALUATION.md, IMPLEMENTATION-CONTRACT.md and
DELIVERY-PLAN.md as needed. Rubric: design 125, planning 100, implementation 100,
reflection 75, presentation/demo 100. No earned score is claimed.

## Paste into a fresh chat

Continue from CURRENT-STATE-HANDOFF.md and DEVELOPMENT-HANDOFF-2026-11-02.md.
The real human-approved test/optimization and failure/replanning/repair chains
are verified; preserve their ignored evidence. Build corpus evaluation and
coherent fresh-clone packaging, then finish/rehearse DEMO-RUNBOOK.md for Lars's
Thursday 5 November 2026 presentation. Fix hardcoded historical IDs/artifact
dependencies so new demos run independently without resetting history. Keep
ADK + LangGraph, exact-patch interactive approvals and Docker boundaries. Do not
simulate user approvals or label cached runs live. Work autonomously until a
genuine human action is needed, with concrete reviewable patches before approval.
