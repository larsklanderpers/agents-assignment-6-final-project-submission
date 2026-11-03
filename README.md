# Review Ledger — Track 5: Code Review & Refactoring

Optional local [read-only dashboard](DASHBOARD.md): run
`.venv\Scripts\python.exe dashboard.py` and open `http://127.0.0.1:8765`.
Approvals remain in the terminal. The pre-dashboard implementation is preserved
at tag `checkpoint/pre-dashboard-20261103`.

Additional work on `hardening/python-intake-evaluation` is documented in
[hardening status](HARDENING-STATUS.md). The established rehearsal/primary
recording remains the bounded baseline; hardening is not silently substituted
for that evidence. See [repository intake and evaluation](HARDENING.md).
The [Luna-authored blinded holdout](HOLDOUT-LUNA-RESULTS.md) records the frozen
review experiment separately, including provisional scores and incomplete labels.

A bounded Python capstone prototype using **Google ADK** for four parallel
specialists, synthesis and patch authorship, and **LangGraph** for persistent
human approval and execution state. Git and a pinned offline Docker runner
provide the local tool integrations. Arbitrary repository/PR intake is unfinished.

Four real human-approved historical operations are preserved: test prerequisite
VERIFIED, optimization VERIFIED, disclosed negative case FAILED, and separate
repair VERIFIED. See [first operation](FIRST-APPROVED-RESULT.md),
[optimization](OPTIMIZATION-RESULT.md), [failure](FAILURE-REPLANNING-RESULT.md),
and [repair](RECOVERY-RESULT.md). Reopening them does not create a live run.

New demonstrations use independent run directories and unique candidates.
Historical approvals, SQLite ledgers, checkpoints, quarantines and logs are
never deleted to create a demo. The implementation is local and has not yet
been published to the GitHub remote; the remote design-only branch is not a
fresh-clone proof of this implementation.

## Observed evaluation

[Corpus comparison and limitations](results/COMPARISON.md): 16 frozen fixtures,
three repeats each, evaluated with parallel specialists and a single reviewer:
**96/96 reviews completed**. Provisional held-out macro precision/recall:
parallel **0.411 / 1.000**, single **0.510 / 1.000**. Both miss the precision
acceptance target. Automatic category/symbol matching still needs human semantic
adjudication; no corpus patch-success score is claimed. All 16 original/corrected
oracle pairs passed their declared contracts in Docker; two authored test mutants
were detected. These oracle tests are separate from agent-authored patch success.

[Evaluation specification](EVALUATION.md) distinguishes implemented measures from
remaining targets. [Packaging validation](PACKAGING-VALIDATION.md) records checks
and their limits. The combined local regression suite has 42 passing tests.

## Setup (tested Windows / Python 3.12)

Required: Python 3.12 with a working bootstrap pip, Git, Docker Desktop with its
Linux engine, and a Gemini API key with access to the configured model.
`requirements-spike.lock` pins the tested package snapshot (ADK 2.13.0,
LangGraph 1.2.18, SQLite checkpointer 3.1.2). It is a version-pinned snapshot,
not a hash-locked cross-platform distribution. Operator locking currently uses
Windows `msvcrt`; Linux/macOS operation is not claimed.

After obtaining the implementation source package or an implementation commit:

```powershell
.\setup.ps1 -Python python
```

If the installed interpreter is not named `python`, pass its full Python 3.12
path. Setup creates a new environment, installs the pinned packages through the
bootstrap interpreter, checks dependencies and creates `.env` from `.env.example`
only if it is absent. Edit `.env` locally: set `GOOGLE_API_KEY` and
`REVIEW_LEDGER_MODEL` (tested alias `gemini-3.8-flash`). Never commit credentials.
An existing configured environment is preserved.

Start Docker Desktop, then prepare the exact image explicitly if it is absent:

```powershell
& 'C:\Program Files\Docker\Docker\resources\bin\docker.exe' pull 'python@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f'
.venv\Scripts\python.exe review_ledger.py doctor
```

Doctor reports only configuration booleans, not credentials. It exits nonzero
for missing prerequisites. It does not make a model request or prove quota.
No automatic image pull occurs during patch execution.

## New demonstration without resetting history

Run commands in this repository's PowerShell terminal:

```powershell
$demoRun = 'my-demo-1'
.venv\Scripts\python.exe review_ledger.py new --run $demoRun
.venv\Scripts\python.exe review_ledger.py reviews --run $demoRun
.venv\Scripts\python.exe review_ledger.py plan --run $demoRun
.venv\Scripts\python.exe review_ledger.py propose-tests --run $demoRun
.venv\Scripts\python.exe review_ledger.py status --run $demoRun
.venv\Scripts\python.exe review_ledger.py review-tests --run $demoRun
```

Creation refuses an existing ID. Without `--run`, `new` prints a generated ID;
use that ID for all later commands. Every run has its own
`artifacts/runs/<id>/run.json`, review/plan outputs and execution candidates.
Status is read-only and never creates a missing ledger. New execution workspaces
use short UUID paths under `artifacts/ws/`; operation evidence records their layout.

The human endpoint displays the exact diff and asks `Your decision:`. Personally
inspect it and type `approve <displayed 12-character patch hash>` only if you
accept it. Alternatives: `reject`, `redirect`, `defer`, `cancel`. Approvals bind
actor, run, exact patch, parent, plan, scope and policy; single use, 30-minute
expiry. A generated candidate is not authorization. No agent/tool enters your
approval. After VERIFIED tests, continue:

```powershell
.venv\Scripts\python.exe review_ledger.py prepare-optimization --run $demoRun
.venv\Scripts\python.exe review_ledger.py review-optimization --run $demoRun
.venv\Scripts\python.exe review_ledger.py prepare-failure --run $demoRun
.venv\Scripts\python.exe review_ledger.py review-fault --run $demoRun
.venv\Scripts\python.exe review_ledger.py replan --run $demoRun
.venv\Scripts\python.exe review_ledger.py review-repair --run $demoRun
```

The deliberately incorrect negative-case patch is disclosed before its own
approval. Its real failed test causes quarantine. Replanning uses actual logs,
invalidates the old candidate and proposes a separately approved repair from the
last VERIFIED parent. The successful optimization remains on its independent
branch. Dependent readiness never means authorization.

The initial fixture and collection-specific policies are intentionally bounded;
this is not a general refactoring service. Failed model output can block a run.
The first new human-approved attempt exposed a Windows path failure and was
quarantined as AMBIGUOUS. The replacement then FAILED on an incorrect model-generated expected order.
[Corrected tests](TEST-EXPECTATION-CORRECTION.md) passed 7/7 in a separate simulated
Docker verification and subsequently passed its real human-approved run.
The optimization also reached real human-approved VERIFIED. The disclosed
negative case then FAILED as expected and live replanning produced plan 4.
The separately approved repair is now VERIFIED; all four real stages have
matching saved bindings, logs, checkpoints and resulting files. No repair approval
is pending in the completed run; see [fresh progress](FRESH-REHEARSAL-RESULT.md).
Its full fresh chain still needs a human dress rehearsal. Original human-approved history remains separately verified.

## Testing and reproducibility

```powershell
.venv\Scripts\python.exe -m unittest test_action_planning test_approval_executor test_optimization_step test_failure_demo test_spike_persistence test_container_boundary test_run_packaging test_long_path_execution test_proposal_checks -q
.venv\Scripts\python.exe -m evaluation.verify_fixtures --output artifacts/evaluation/my-oracle-check
.venv\Scripts\python.exe -m evaluation.run --manifest evaluation/manifest.json --seed 505 --repeats 3 --output artifacts/evaluation/my-parallel
.venv\Scripts\python.exe -m evaluation.run --manifest evaluation/manifest.json --seed 505 --repeats 3 --mode single --output artifacts/evaluation/my-single
```

Use a new output directory for every attempt. Corpus labels/corrections/hidden
assertions are in the frozen manifest, never in model snapshots; the model sees
only source and visible tests. Do not rebuild or alter the labels after results.
Model runs use the configured API and incur usage. Frozen outputs, per-run JSON,
category counts, CSV, token metadata, latency and failure accounting are in
`results/`; original local artifacts remain intact. Fixed-order non-replanning
comparison and corpus repair evaluation remain unimplemented.

For read-only local historical evidence:

```powershell
.venv\Scripts\python.exe saved_evidence.py
```

It checks recorded bindings/log hashes and labels everything SAVED. A fresh
package has no historical ignored ledgers and reports their absence honestly.
The old `approve-*.cmd` launchers explicitly target historical gates.

## Packaging, presentation and submission

```powershell
.venv\Scripts\python.exe package_source.py --output artifacts/packaging/my-source.zip
```

This exports allowlisted source, documents and synthetic corpus results with a
SHA256 file manifest. It excludes `.env`, `.venv`, `.git`, all `artifacts/` and
historical private evidence. LF normalization plus `.gitattributes` keeps corpus
hashes stable through Windows Git checkouts. See [packaging proof](PACKAGING-VALIDATION.md).
A local source-only Git clone was used for validation; no remote publication or
instructor access is implied by that test.

[Thursday checklist](THURSDAY-DEMO-CHECKLIST.md) lists what remains.
[Thursday 5 November runbook](DEMO-RUNBOOK.md) gives commands, prompts, screen
locations, live/prepared/saved labels, a 9:30 schedule and recovery routes. A full
spoken <=10-minute rehearsal and final recording are **pending**. Recording link:
**not yet available**. Confirm Canvas deadline, instructor access, page limits
and two-track handling before submission.

Design and delivery: [architecture](ARCHITECTURE.md),
[implementation contract](IMPLEMENTATION-CONTRACT.md),
[reflection](TECHNICAL-REFLECTION.md), [delivery plan](DELIVERY-PLAN.md),
[requirements](CAPSTONE-REQUIREMENTS.md), [current handoff](CURRENT-STATE-HANDOFF.md).
The architecture/reflection still need typesetting and page-count checks.

AI implementation assistance is permitted; the student must explain every line.
Original prototype code uses documented ADK structured-output and LangGraph
interrupt patterns cited in source and architecture. No tutorial implementation
was copied. No automatic merge, push or deployment is provided.
