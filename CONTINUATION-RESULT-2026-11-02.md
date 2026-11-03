# Continuation results and remaining human gates — 2 November 2026

**Latest new-context handoff:** [REHEARSAL-HANDOFF-2026-11-03.md](REHEARSAL-HANDOFF-2026-11-03.md).
The dress rehearsal is ready, but the timer has NOT started. Its characterization
approval is already VERIFIED; do not ask for it again. Next is physical readiness,
then the 0:00 speaking cue and deliberate fault approval at 2:20. Older pending
states below are chronological history.


ACTIVE REHEARSAL UPDATE: thursday-dress-20261103-01 characterization is now
real interactive VERIFIED (eae1ddf125954a0ea3565538bd2f80b3), seven passes.
Optimization proposal is prepared and intentionally NOT approved in this short
route. Fault candidate demo-fault-e292e414e1 is pending, prefix 99d40a18b4f6;
separate simulated preflight confirmed seven tests/one expected nested-list
TypeError and quarantine. Actual optimization/fault ledgers have zero decisions
and operations. Timer has NOT started. Next: user opens cue sheet/screens and
says ready to start; coach gives 0:00 speaking cue, then 0:45 roles, 1:35 plan,
2:20 fault approval. User's stopwatch measures actual full duration including
waiting/chat pauses. Do not call anything live from the completed prior run.
After actual fault failure, run live replan for THIS run and prepare/verify its
new repair, then ask its independent human approval around the 5:10 target.
See REHEARSAL-SESSION-2026-11-03.md. Google reflection link remains in
REFLECTION-WORKING-COPY.md; preserve user cloud edits. Separate untouched
Thursday run still to prepare after the dress rehearsal.


ACTIVE TASK - 3 November: user requested a fresh Thursday demo and coached timed
rehearsal, plus a Google Drive reflection link. New run thursday-dress-20261103-01
has fresh four-agent reviews, validated plan and exactly seven new tests. Exact
proposal passed a separate simulated Docker check; real approval is pending unless
latest ledger says otherwise. Candidate candidate-7da399bfc64b-exec-v1, prefix
2c21598cb9cd. An asynchronous prompt already asked Lars to run review-tests for
that ID; do not enter a decision. Timer remains STOPPED for setup. After VERIFIED,
prepare optimization (proposal only, no extra human approval needed), prepare and
check the fault gate, then coach the 9:30 rehearsal with explicit live fault and
repair approvals. Prepare another untouched run for Thursday after this dress
rehearsal completes. Preserve every older verified/failed run.

Google reflection created/readback-verified in ChatGPT folder: see
REFLECTION-WORKING-COPY.md for its link. It contains full editable working material,
not a final page-count claim, and does not auto-sync. Do not overwrite user edits.
Session cues and state: REHEARSAL-SESSION-2026-11-03.md and the new run's
rehearsal-session.json. Actual full spoken duration/recording still unmeasured.


AUTHORITATIVE UPDATE - 3 November 2026: the repair is real human-approved
VERIFIED in operation bde81e424c184be6b33ecd79b92fec35 (seven tests + thirteen
checks). Read-only audit matched all four real stages' bindings, consumed
interactive approvals, both log hashes, terminal checkpoints and actual files to
recorded trees. Audit did not change manifests/patches/ledgers/checkpoints. Earlier
unsuccessful attempts' 79 files remain unchanged. completion.json is retained in
the run's artifacts/failure-demo directory. Follow-up is eligible for proposal
only, not authorized/executed; do not build it for this demo. No repair approval
is pending in this completed chain. Use THURSDAY-DEMO-CHECKLIST.md and the updated
DEMO-RUNBOOK.md for timed live rehearsal, recording, page counts and submission.
Older pending-state notes below are historical. Use a new ID for a fresh live
segment and keep this run as labeled saved fallback.


CURRENT UPDATE - 3 November 2026: real negative-case operation
22f6b9be80134420b4d64c92af8659d0 FAILED with expected nested-list TypeError and
is quarantined. Live replan now at version 4. Repair demo-repair-c136cbeea2 is
pending human review (review-repair, approval prefix a0540b3e4776); separate
simulated preflight passed seven tests plus thirteen checks. Stale approval was
rejected with no extra operation; follow-up stays blocked. Full suite: 42 passed
in 50.089s. Read REPAIR-REVIEW-2026-11-03.md and DEMO-RUNBOOK.md first; older
pending-stage entries below are historical. Preserve both replan attempts/raw
outputs, formatting rejection and normalized-source provenance. The original
raw output of the first rejected plan was not retained; that limitation is recorded.


Latest state: optimization also reached real human-approved VERIFIED, operation
14ba9fa431624649bfd5771169957cb3 (seven tests + thirteen checks). Next pending
human gate is the disclosed negative case: review-fault for this run, approval
prefix 99d40a18b4f6. Expected FAILED with nested-list TypeError. Independent
simulation confirmed that failure, but the actual fault ledger has zero operations.
After the actual human-approved failure, run live replanning against its real logs.
See FRESH-REHEARSAL-RESULT.md; older pending-state entries below are chronological.
Working docs now postdate r3; regenerate the final archive after recovery.


Current update: corrected tests are human-approved VERIFIED in operation
`a27c01f604c34003a1bb1124713b81d3` (seven passes). The pending next gate is
`lookup-02b915e9445a`, approval prefix `f98f895977a0`; independent simulated
preflight passed seven tests plus thirteen checks. Negative-case proposal is
prepared but unexecuted. Read FRESH-REHEARSAL-RESULT.md and the updated runbook
before using any older pending-state instructions below, which are chronological
history. The trusted-harness path fix passed six focused regression tests.


This updates `DEVELOPMENT-HANDOFF-2026-11-02.md`. Preserve that historical
handoff and all ignored evidence. Current source is local/uncommitted on
`implementation/first-patch`; the remote still contains the design base.

## Completed autonomous work

- `review_ledger.py` creates isolated named/UUID runs, invokes fresh reviews,
  planning and proposals, exposes read-only status, and routes exact-patch
  interactive approvals. New runs do not depend on historical artifact IDs.
- `runtime_paths.py` selects the current run and validates its candidate location.
  Legacy launchers remain labeled historical. Fresh failure plans carry the
  actual original finding references rather than assuming reviewer output order.
- Frozen 16-fixture corpus (6 development, 6 renamed held-out, 4 controls), seed
  505. Manifest SHA256:
  `730e71e27e42ee349bf02185a608d4c2add52ac0f4d0c6507351ed01e1e3ad70`.
  Do not regenerate/tune it after evaluation. Human label/adjudication review is
  pending; original machine labels and scores must remain available.
- Live finding evaluation: 48 parallel-mode + 48 single-reviewer attempts,
  all complete. Held-out macro precision/recall: parallel 0.411/1.000,
  single 0.510/1.000. Precision target missed. Published raw synthetic outputs,
  usage, latency, per-category counts/CSV and comparison: `results/`.
  Token totals: 101,708 parallel versus 34,945 single. Monetary cost unknown.
- Docker oracle checks: 16/16 original/corrected contract pairs and 2/2 authored
  mutants detected. These are not agent patch-success metrics. Corpus patch
  attempts: 0; repair/approval/trace/case-completion metrics N/A. Fixed-order
  non-replanning baseline remains unimplemented.
- `setup.ps1`, source exporter, `.gitattributes` LF policy and package validator.
  New independent environment and actual source-only local Git clone installed
  the exact lock successfully; `pip check` passed. No credentials/history copied.
  Final proof is recorded under `artifacts/packaging/`.
- Detailed `DEMO-RUNBOOK.md` for Thursday 5 November, with exact operator steps,
  human prompts, expected outcomes, screen/evidence locations, 9:30 schedule,
  truthful prepared/live/saved labels and error/offline/restart routes.

## New human rehearsal: retain both attempts

Run: `packaging-rehearsal-20261102`.

Fresh reviews/plan/test author generated patch
`e2a9c4f3541ff40573cedc4f1276d688ca75946f76073e1ec2b349c97b1f395e`.
Lars entered a real interactive approval. The operation
`728750cb5b444beda6a05698bbe0e1ee` became **AMBIGUOUS** after apply because
nested Windows paths hid the test file from Python enumeration. Its ledger,
checkpoint, zero-test baseline log and quarantined applied bytes are retained.
Do not reset that terminal operation or transfer its consumed grant.

Fix: new operations use UUID workspaces under `artifacts/ws/<op-id>/` with
validated `workspace-location.json` in their operation evidence directory.
Historical layouts still resolve. Win32 extended paths protect deep log paths;
Git receives normal Windows paths. Docker result parsing tolerates stdout/stderr
interleaving, while rejecting duplicate result markers and invalid counts.
Separate simulated-approval integration ran real Git/Docker, seven tests and
safe replay with deep operation evidence; no real approval was simulated.

The replacement `candidate-93a15f976a12-exec-d24e41f5` was personally approved
and FAILED in operation `7e83013f61a549dd98bb5ebee2ffc7e6`: seven tests, one
model-authored expected-order error. Its ledger/log/quarantine are preserved.
Correct expectation for the duplicate example is `[1, 1, 3, 1]`, not `[1, 1, 1, 3]`.

Current candidate: `candidate-32a6e3d26914-exec-v1`; patch hash
`177fba7497b1b2d26c2f800790685240e9acfea46df7c7d832672e12bd815b01`.
All seven corrected tests passed in an independent, explicitly simulated approval
fixture with real Git/Docker **before** this new gate was prepared. Static checks
now reject incorrect literal examples before preparation. All 79 earlier evidence
files matched before/after; do not transfer either consumed grant.
Read TEST-EXPECTATION-CORRECTION.md and current status before requesting a decision.

```powershell
.venv\Scripts\python.exe review_ledger.py review-tests --run packaging-rehearsal-20261102
```

After personal diff review, the current exact decision is `approve 177fba7497b1`.
The new real endpoint has no approval or operation until the human acts.

Once replacement is VERIFIED, autonomously prepare the fresh optimization and
negative-case gates using the run-specific entrypoint. Each execution still needs
its own human decision. Do not reuse the four historical approvals. Follow
DEMO-RUNBOOK.md; do not claim the new full chain passed from old history.

## Verification and remaining delivery work

Original 32-test combined suite passed (63.040s); added long-path execution and
marker parser regressions bring the suite to 34. Final combined suite passed 34 tests in 46.148s; clean source-only clone passed
34 tests in 50.047s, verified all 211 source hashes, and ran fresh review/plan/
proposal to an unapproved gate in 52.906s. Logs and clone proof live under `artifacts/packaging/`. All failed diagnostic test attempts are
retained; only logs explicitly showing OK count as passes. Preserve original
historical runs; read-only saved-evidence checks still match all bindings/logs.

Remaining: finish the fresh human-approved chain; measure an actual spoken
<=10-minute dress rehearsal and record it; human semantic corpus adjudication;
corpus patch/planning evaluation; arbitrary PR intake; final source publication
and instructor access; typesetting/page counts; Canvas deadline/two-track rules.
No implementation has been pushed, and no completed recording is claimed.

Use `README.md`, `PACKAGING-VALIDATION.md`, `results/COMPARISON.md` and
`DEMO-RUNBOOK.md` as the current operational documents. The original design
documents now carry current-status notices and observed reflection updates.

## Latest test-expectation correction verification

Updated full suite: 39 tests passed in 48.219s. All seven exact corrected tests
passed in a separate simulated preapproval Git/Docker run; both earlier attempts'
79 evidence files remained unchanged. Current human gate is
candidate-32a6e3d26914-exec-v1, approval prefix 177fba7497b1. Its real operation
remains unapproved until Lars acts. See TEST-EXPECTATION-CORRECTION.md and the
updated runbook. The r2 delivery ZIP supersedes the prior ZIP for source delivery;
all older archives and clone proof artifacts are retained.

## Reflection capture

At Lars's explicit request, TECHNICAL-REFLECTION.md now captures both actual
rehearsal failures, the missed generated-test expectation, the distinction between
authorization and correctness, repeated human-review effort, earlier static and
simulated verification, and preservation of all 79 evidence files. Keep these
lessons alongside the measured corpus accuracy/token tradeoffs in the final
reflection. Add the eventual human-gated result and timed rehearsal outcome;
condense the working material to the agreed 1–2 typeset pages before submission.
Regenerate the delivery archive after final document edits; the retained r2 ZIP
predates this reflection addition.

Latest suite: 40 tests passed in 52.223s. Next approval is the real optimization
gate (review-optimization, prefix f98f895977a0), independently preflighted in
simulation. The negative case is prepared but has no decision or operation.
The r3 source archive supersedes r2 for delivery and includes the reflection.
