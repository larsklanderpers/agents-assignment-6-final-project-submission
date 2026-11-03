# Review Ledger — presenter and operator runbook

Current guided session: [REHEARSAL-SESSION-2026-11-03.md](REHEARSAL-SESSION-2026-11-03.md),
using new run `thursday-dress-20261103-01`. Approval 1 is characterization during
preparation with the clock stopped; timed approvals are the fault at about 2:20
and the separately authored repair at about 5:10. The session is not timed yet.
The editable reflection link is in REFLECTION-WORKING-COPY.md. The completed
`packaging-rehearsal-20261102` remains labeled saved evidence.


Presentation: **Thursday 5 November 2026, Australia/Sydney**. Maximum combined
presentation/demo/recording: 10 minutes. Target: 9:30, leaving 30 seconds reserve.
Canvas deadline is separate and remains unconfirmed.

## What has actually been tested

- The completed fresh run `packaging-rehearsal-20261102` contains real interactive
  approvals for VERIFIED characterization, VERIFIED optimization, the disclosed
  FAILED negative case and VERIFIED repair. The failed workspace remains
  quarantined. Earlier unplanned failed attempts and all original history remain.
- On 3 November, read-only checks matched manifest/approval bindings, both log
  hashes, completed checkpoints and actual workspace bytes to recorded trees.
  The real repair passed seven tests plus thirteen checks. Earlier unsuccessful
  attempts' 79 files remained unchanged. See FRESH-REHEARSAL-RESULT.md.
- Independent simulated preflights are separate evidence. They never supplied a
  real approval or unblocked the follow-up. That follow-up is now eligible only
  for proposal and remains unauthorized/unexecuted; it is not needed for the demo.
- Latest implementation regression: 42 tests passed. The earlier source-only
  clone proof passed 34 tests and 211 exported hashes; the 52.906-second automated
  new/review/plan/propose/status route is not a spoken presentation timing.
- A complete spoken <=10-minute rehearsal and final recording remain unmeasured.
  The 9:30 schedule below is a production target, not an achieved duration.

[Thursday checklist](THURSDAY-DEMO-CHECKLIST.md) separates ready evidence from the
remaining live-run preparation, timing, recording and submission tasks.


## Screen layout and evidence

Use a readable font (at least 18pt); close unrelated windows and notifications.
Never open `.env`, credentials, provider debug dumps or the parent keys file.
Have three windows ready:

1. Architecture diagram in `ARCHITECTURE.md`, then corpus report in
   `results/parallel/REPORT.md` and comparison in `results/COMPARISON.md`.
2. PowerShell, working directory this repository. Commands below assume this
   directory and use `$demoRun` for the chosen run ID.
3. Editor showing the selected run's `candidate.patch`, `manifest.json`, failure
   `candidate.log`, `current-plan.json` and `replanning-evidence.json`.

For fresh runs, all paths are beneath `artifacts/runs/<run-id>/artifacts/`:

| Stage | Evidence location |
|---|---|
| Four fresh reviews | `live-spike/result.json` (four roles, source hash, overlap, spans) |
| Validated plan | `plan-spike/result.json` (dependencies and derived readiness) |
| Human test gate | `first-patch/<candidate-id>-exec-v1/` (see `run.json` for exact name) |
| Optimization | `optimization/reviews.json`, `plan.json`, `candidate/` |
| Failure | `failure-demo/fault/operations/<operation-id>/candidate.log` |
| Quarantine | `artifacts/ws/<operation-id>/quarantined_workspace/` for new operations |
| Replan | `failure-demo/plan-v3.json`, `plan-v4.json`, `replanning-evidence.json` |
| Separate repair gate | `failure-demo/repair/` |

Each execution candidate holds `ledger.sqlite`, `checkpoint.sqlite`, a manifest
and exact diff. Operation directories hold baseline/candidate logs and disposable
workspace-location markers. New short UUID workspaces are under
`artifacts/ws/<operation-id>/`; historical workspaces keep their original layout.
Keep all of them; SQLite files are evidence, not files to reset.

## Day-before preparation (outside recording)

Read the README setup instructions; run the environment check:

```powershell
.venv\Scripts\python.exe review_ledger.py doctor
.venv\Scripts\python.exe -m unittest test_action_planning test_approval_executor test_optimization_step test_failure_demo test_spike_persistence test_container_boundary test_run_packaging test_long_path_execution test_proposal_checks -q
.venv\Scripts\python.exe saved_evidence.py
```

Doctor must exit 0, with Python 3.12, Git, local model/key configuration and the
pinned Linux image available. The image is never pulled automatically during
execution. If absent, explicitly prepare it outside recording:

```powershell
& 'C:\Program Files\Docker\Docker\resources\bin\docker.exe' pull 'python@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f'
```

Create a **new** run for every full dress rehearsal. These commands do real
model work and incur provider usage; they do not authorize any patch:

```powershell
$demoRun = 'thursday-dress-1'
.venv\Scripts\python.exe review_ledger.py new --run $demoRun
.venv\Scripts\python.exe review_ledger.py reviews --run $demoRun
.venv\Scripts\python.exe review_ledger.py plan --run $demoRun
.venv\Scripts\python.exe review_ledger.py propose-tests --run $demoRun
.venv\Scripts\python.exe review_ledger.py status --run $demoRun
```

Expected: creation refuses an existing ID; review prints `pending_gate: true`,
four role counts and `overlap: true`; planning shows characterization ready and
lookup refactoring blocked; proposal prints a unique candidate and pending gate.
Status lists hash matches and no operations before approval. All four specialists
must complete; a partial or invalid response blocks the path. Source is the
explicit ten-line synthetic fixture; arbitrary repository/PR intake is unfinished.

For a short stage demo, prepare reviews/plan/test gate before recording and say
“These reviews were generated earlier; this approval and execution are live.”
After personally reviewing and approving tests, prepare the optimization outside
recording. Do not approve it merely to prepare the negative case: preparation of
the optimization candidate is enough, but the characterization must be VERIFIED.

```powershell
.venv\Scripts\python.exe review_ledger.py review-tests --run $demoRun
.venv\Scripts\python.exe review_ledger.py prepare-optimization --run $demoRun
.venv\Scripts\python.exe review_ledger.py prepare-failure --run $demoRun
```

`prepare-failure` deliberately proposes an incorrect set conversion on an
independent disposable branch. It never changes the successful optimization.
The negative case must be described before approval and must never be adopted.
Each exact patch still requires its own human decision.

## Exact human interaction

Every `review-*` command must run in a normal local interactive terminal.
Do not pipe input, use a model to answer, or reuse a saved approval string.
The endpoint prints operator, candidate, plan version, parent commit/tree, full
patch hash, risk, acceptance, provenance, exact diff and these choices:

```text
Choices: approve <first 12 characters of THIS patch SHA256> | reject | redirect | defer | cancel
Your decision:
```

Read the diff and acceptance contract. Type the displayed `approve ...` only if
you accept that exact proposal. The prefix changes with new generated patches.
`approve` without the hash is rejected. `redirect` asks `New constraints:`;
enter nonempty constraints, after which no edit executes. `defer`, `reject` and
`cancel` also do not apply the patch. Deferral has no expiry. Issued approvals
expire after 30 minutes; a plan/parent/policy/patch change invalidates them.

For the existing local rehearsal, characterization is now **VERIFIED** under
real human operation `a27c01f604c34003a1bb1124713b81d3`. Its seven tests passed.
Reopening `review-tests` displays that saved result; it does not start a new run.
Both earlier unsuccessful attempts remain preserved.

The optimization is also now **VERIFIED** under real human operation
`14ba9fa431624649bfd5771169957cb3`: seven tests plus thirteen checks passed.
Reopening `review-optimization` shows that saved outcome.

The negative-case operation `22f6b9be80134420b4d64c92af8659d0` subsequently
FAILED with the expected nested-list TypeError and remains quarantined. Live
replanning moved plan 3 to 4; the old fault gate is now invalid for execution.

The repair is now **VERIFIED** under real interactive operation
`bde81e424c184be6b33ecd79b92fec35`: seven tests plus thirteen checks passed.
There is no pending approval in this completed chain. Reopening `review-repair`
shows a saved result, not a fresh execution. The follow-up is eligible for a
proposal only and remains unauthorized/unexecuted.

For the live demonstration, use a different run ID and the preparation sequence
above. Stop that new run at its own pending fault gate before recording. Do not
reuse a completed run's approval prefix or delete history to recreate a gate.
The new fault and new repair each need their own personal exact-patch decision.

To display the completed chain as saved evidence in PowerShell:

```powershell
$completedRun = Get-Content -Raw -LiteralPath 'artifacts/runs/packaging-rehearsal-20261102/artifacts/failure-demo/completion.json' | ConvertFrom-Json
$completedRun.operations | Select-Object stage, state, operation_id
```

Say: "These are the saved human-approved operations audited on 3 November."
The audit checked bindings, hashes, checkpoints and resulting files without
rerunning them. [Fresh results](FRESH-REHEARSAL-RESULT.md) summarizes the four real
operations; [repair review](REPAIR-REVIEW-2026-11-03.md) retains preparation history.


## When a generated characterization test fails

Read the real test log and trace concrete inputs by hand against the documented
contract. A failing test can have an incorrect expectation; do not change correct
production behavior to satisfy it. Here, left-input order requires `[1, 1, 3, 1]`,
not grouping all ones before the three. This was an actual model test-authoring
error, separate from the later deliberate negative-case optimization demo.

Preserve the terminal attempt and its approval. Propose a new test patch, run the
static literal-example guard, and verify its exact bytes in a separately labeled
simulated fixture before presenting a new human gate. `amend_tests.py` automates
that sequence and refuses to prepare a gate if container verification fails.
No candidate code executes during the static check. Its scope is bounded literal
examples; the actual isolated test run remains necessary.


## Full operator sequence (including optional optimization)

After test approval: expect VERIFIED with at least seven tests, zero failures,
errors or skips. A zero-test baseline is explicitly `no_tests`.

```powershell
.venv\Scripts\python.exe review_ledger.py prepare-optimization --run $demoRun
.venv\Scripts\python.exe review_ledger.py review-optimization --run $demoRun
.venv\Scripts\python.exe review_ledger.py prepare-failure --run $demoRun
.venv\Scripts\python.exe review_ledger.py review-fault --run $demoRun
```

Optimization requires seven unchanged tests plus thirteen reference checks and
measured improvement on the single integer workload. The negative case expects
FAILED: the nested-list case raises a real `TypeError` (`unhashable type: list`).
Open its actual candidate log. Show the quarantined workspace and blocked
descendant; the intentionally incorrect diff was disclosed **before** approval.
The command may exit normally while reporting operation state FAILED; inspect
the operation outcome rather than treating process exit alone as acceptance.

```powershell
.venv\Scripts\python.exe review_ledger.py replan --run $demoRun
.venv\Scripts\python.exe review_ledger.py review-repair --run $demoRun
.venv\Scripts\python.exe review_ledger.py status --run $demoRun
```

Replan consumes actual failure logs in fresh model calls; expect plan version
3 → 4, failed action deferred, repair based on the VERIFIED test-bearing parent,
descendant redirected to depend on repair, and old approval replay rejected
without another operation. Inspect the new diff and enter its **new** approval
prefix. Successful repair requires seven tests plus thirteen checks. The
follow-up becomes eligible for proposal; it is not automatically authorized or
executed. SQL and public API style issues remain unresolved.

## 9:30 presentation schedule and speaking notes

| Clock | Screen/action | Speaking notes |
|---|---|---|
| 0:00–0:45 | Architecture diagram | “Review Ledger reviews code and proposes a dependency plan. Human decisions gate every edit, including tests and recovery. This is a bounded synthetic Python prototype.” |
| 0:45–1:35 | Four review outputs, source-line evidence | “Four ADK specialists independently inspect the same snapshot: security, performance, style and test gaps. Their agreement is not proof; strict local validation checks identities and cited source lines. These particular reviews are saved from preparation.” |
| 1:35–2:20 | Ranked plan | “LangGraph owns durable state and approval interrupts. The planner proposes a DAG. Deterministic rules enforce characterization first and block unresolved conflicts. A priority score cannot grant authorization.” |
| 2:20–3:10 | Exact prepared fault diff and human gate | “Characterization was already separately approved and verified. This is a disclosed negative-case branch. The set conversion is deliberately wrong for nested lists. I am approving only this exact patch for the disposable demonstration.” Enter the current hash only after inspection. |
| 3:10–4:00 | Actual failed test/log and quarantine | “The container ran the real test. Nested lists cannot be hashed. Failure is retained, the workspace is quarantined, and dependent work remains blocked. There are no host mounts, credentials or network in this test container.” |
| 4:00–5:10 | Run replan, show v3/v4 and stale rejection | “The planner receives actual failure evidence. It abandons the failed action, returns to the last verified parent and redirects the descendant to a new repair. The old approval cannot authorize this revised plan.” If provider exceeds 45 seconds, use the labeled saved route below. |
| 5:10–6:25 | New repair diff and live human approval | “This guarded fast path preserves the original loop as fallback. This is a new patch with a new hash. Its approval is independent of the failed step.” Review the diff and acceptance, then decide. |
| 6:25–7:10 | Repair outcome | “The seven tests and thirteen additional comparisons pass. Any timing improvement applies only to the measured integer case and uses extra memory. The next step is merely eligible for proposal.” |
| 7:10–8:05 | Ledger/status and saved-evidence distinction | “SQLite records the exact binding and operation outcome. Checkpoints survive restart; reconciliation prevents duplicate application. Saved historical runs are labeled separately and never reset for a fresh demonstration.” |
| 8:05–9:05 | Corpus and comparison reports | State the actual held-out precision/recall and FP counts from `results/COMPARISON.md`. “Six development fixtures, six tiny held-out variants, four controls, three repeats. Scores are automatic category/symbol matches pending human semantic adjudication. Finding evaluation does not establish corpus patch success.” |
| 9:05–9:30 | Reflection/closing | “ADK gives role-based parallel reasoning; LangGraph gives persistent human control. The integration adds maintenance cost. Broader PR intake, stronger identity, independent corpus adjudication and full corpus repair evaluation remain future work.” |

Do not read setup commands aloud. Keep lengthy JSON collapsed to the relevant
fields. Pre-open evidence files so directory navigation does not consume stage
time. No speedup is a general complexity claim. No earned rubric score is claimed.

## Failure and offline routes

| Trigger | Tested/safe operator response |
|---|---|
| Network/model timeout or invalid output | State “live reasoning did not finish”; preserve its run directory. Do not invent a complete review. Switch to published saved evidence. A retry is another disclosed attempt, preferably a new run. |
| Missing Docker/image | Doctor exits nonzero; start Docker Desktop or explicitly pull the pinned image outside recording. Do not execute tests on the host as a substitute. |
| Approval terminal closed at pending gate | Reopen the same `review-*` command. Saved candidate/checkpoint survive; no approval was granted by closing it. |
| Crash after apply | Reopen the same command; existing intent/tree reconciliation governs resumption. Never delete ledger/checkpoint/lock files to force a new application. If lock appears stale or state is ambiguous, stop and use saved evidence. |
| Completed gate reopened | It shows the existing outcome; say “saved completed operation.” It is not a fresh execution. |
| Fault gate reopened after replan | Version-3 candidate is invalid; inspect it as saved evidence. Continue only through `review-repair`. |
| Candidate or parent changed | Stop; fresh review/proposal and fresh approval required. Do not edit manifest hashes. |
| Repair fails | Keep FAILED evidence/quarantine; do not call it recovered. Switch to labeled historical repair outcome. |
| Time reaches 8:30 with pending tools | Stop waiting and summarize actual state, then show saved result with explicit label. Finish before 10:00. |

Offline command on the development computer:

```powershell
.venv\Scripts\python.exe saved_evidence.py
```

Say: “I am now showing saved human-approved evidence from 2 November, not a new
live operation.” The script reads ledgers in read-only mode and checks recorded
manifest bindings and log hashes. It does not rerun tests or certify a current
workspace tree. In a fresh source package the ignored ledgers are absent;
use `FIRST-APPROVED-RESULT.md`, `OPTIMIZATION-RESULT.md`,
`FAILURE-REPLANNING-RESULT.md`, `RECOVERY-RESULT.md` and published corpus reports.
Do not imply that a source package contains the private local evidence.

## Dress rehearsal and recording acceptance

Start an actual stopwatch before the first spoken sentence. Record the whole
combined presentation, including human waiting and any tool failures. Fill the
following only after doing it:

| Field | Actual result |
|---|---|
| Date/run ID | Pending human dress rehearsal |
| First sentence → final sentence | Not yet measured |
| Fresh vs prepared vs saved sections | Record explicitly |
| Real failure and separate repair execution evidence | VERIFIED in saved run; showing/recording them in the final presentation remains pending |
| Total <=10:00 | Not yet verified |
| Recording URL / Canvas upload | Pending |

If over time, shorten narration or explicitly use a saved section; never hide
waiting while labeling the entire result live. Before submission verify audio,
readability, instructor repository access, the actual Canvas deadline and the
recording link. Packaging source is not publication: implementation is local
until reviewed, committed and pushed to the chosen accessible repository.

## Remaining work for Thursday

Follow THURSDAY-DEMO-CHECKLIST.md: prepare a new pending live run, measure the
whole spoken rehearsal <=10 minutes, finish/page-check the architecture and
reflection, record the combined demo, publish the accessible implementation and
recording link, and confirm Canvas/page-limit/two-track rules. State the corpus
precision miss and unmeasured corpus repair/adjudication limits plainly.
