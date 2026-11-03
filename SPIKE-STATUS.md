# Local feasibility work — 30 October 2026

The nine design documents were fetched through the authenticated GitHub connector.
This directory is a document snapshot, not a Git clone; Git history is unavailable
until command-line authentication is configured. No remote changes were made.

Accepted scope: personal developer workflow; local CLI; pinned local repository
first; characterization test followed by a dependent lookup optimization; injected
verification failure and replanning. ADK and LangGraph remain selected.

Host inspection found Git and bundled Python 3.12.14. GitHub CLI and Docker were
not available on PATH. Unauthenticated cloning returned repository not found.
Container execution remains blocked; no untrusted repository code has been run.

## Observed results

- 2 November: the separately approved demo repair reached VERIFIED with 7 tests
  and 13 reference checks passing. Median bounded integer timing was 94.421 ms
  before / 0.527 ms after. Integrity and checkpoint checks passed; the failed
  workspace remains quarantined. Readiness was recomputed from the real verified
  ledger: the dependent follow-up is now eligible, not approved/executed.
  `RECOVERY-RESULT.md` records completion of the bounded failure/replanning demo.

- 2 November: the human-approved negative case produced the real nested-list
  TypeError (6 passes, 1 error), exited 1 and was quarantined as FAILED. Evidence
  and checkpoint agree. Live planner/patch-author calls produced revision 4 and
  a guarded correction. Old-approval replay was rejected; descendant remains
  blocked and repair remains unapplied/unexecuted pending a separate decision.
  See `FAILURE-REPLANNING-RESULT.md`.

- Controlled failure/replanning branch prepared from the accepted seven-test
  tree, preserving the successful optimization. A disclosed proposal-layer fault
  awaits exact interactive approval; its descendant is blocked. Three policy
  tests passed. No real failure result or replanned success is claimed yet.
  See `FAILURE-DEMO-WALKTHROUGH.md`.

- The dependent optimization subsequently completed with one interactive approval
  and one VERIFIED operation. Seven tests and thirteen reference checks passed;
  the integer-case timing median improved from 115.379 ms to 0.620 ms. Binding,
  log digests, accepted tree and completed checkpoint agree. Parent remains clean.
  See `OPTIMIZATION-RESULT.md`; this supersedes its pending-approval notes below.

- Dependent optimization prepared against the first VERIFIED tree. Four fresh
  reviews, plan revision 2 and a new ADK-authored six-line source patch are
  persisted. The restricted fast path retains the original loop as fallback.
  Twenty planning/approval regressions and two simulated source-patch checks
  passed; extended Docker checks passed only on the accepted baseline (7 tests
  plus 13 reference comparisons). Candidate remains unapplied/unexecuted pending
  a new interactive approval. See `OPTIMIZATION-REVIEW.md`.

- First real interactive approval completed: one consumed approval, one VERIFIED
  operation, seven tests passed in the isolated container. Independent inspection
  verified approval bindings, log hashes, resulting tree and completed checkpoint;
  the original baseline remains clean. See `FIRST-APPROVED-RESULT.md`. This
  supersedes the pending-real-approval status below for this candidate only.

- Approval/isolated execution slice is implemented for the first test candidate.
  Twelve simulated approval/recovery tests passed; real Docker checks passed
  nine isolation probes and verified explicit zero-test baseline reporting.
  Candidate `candidate-c2a7ed975417-exec-v1` binds the finalized runner policy.
  The real patch remains pending human approval. See `APPROVAL-WALKTHROUGH.md`.

- 1 November: authenticated repository history is now present in the original
  project folder, on `implementation/first-patch` from `4c4ca01`. Local work,
  environment and artifacts were preserved. GitHub CLI sign-in and Docker are
  operational. This supersedes earlier unavailable-Git and snapshot-only notes.
- The real patch-author agent prepared the first test-only candidate. Syntax and
  Git apply-check passed; the target baseline remains clean with no test file
  applied. The candidate is persisted at a pending review interrupt. See
  `FIRST-PATCH-REVIEW.md` for exact identity, coverage and remaining execution gates.

- 1 November 2026: Docker Desktop 4.97.0 / Engine 29.9.2 is reachable using
  `desktop-linux` (linux/amd64). Docker's hello-world container exited 0 with
  networking disabled, read-only root filesystem, UID/GID 65534, all capabilities
  dropped, no-new-privileges, 64 MiB memory, 0.5 CPU and 32-process limit; no host
  mounts or secrets. Image digest:
  `sha256:c567b231f65614688711a75f31518a064258a51d442117a3e771a3a8fdba78ef`.
  This supersedes the earlier unavailable-Docker host finding. The actual Python
  test-runner image and source export boundary still need implementation and
  verification. The restricted tool environment cannot access Docker's local
  pipe; the approved engine-access check succeeded. GitHub CLI remains absent.

- Installed Python 3.12.14, google-adk 2.13.0, LangGraph 1.2.18 and
  langgraph-checkpoint-sqlite 3.1.2 in `.venv`; full package snapshot is in
  `requirements-spike.lock`. `pip check` reports no broken requirements.
- Four deterministic ADK BaseAgent fixtures ran through ParallelAgent with
  overlapping execution intervals. Outputs were validated with Pydantic and
  matched to unique specialist IDs. These are not LLM reviews.
- The custom adapter returned their results into LangGraph. A SQLite-backed
  interrupt persisted the results and pending gate across separate processes.
- `python -m unittest test_spike_persistence -v`: PASS, one multi-process
  integration test in 30.133 seconds. It checked pending-state recovery, rejection
  after restart, duplicate-start rejection and duplicate-resume rejection.
  It does not prove crash recovery after patch application or concurrent locking.
- The restricted execution environment stalls Python's asyncio socketpair setup.
  The same experiment passed with local loopback access enabled. No model service
  or untrusted repository code was invoked.
- ADK 2.13.0 warns that ParallelAgent is deprecated in favor of Workflow.
  Keep this compatibility experiment pinned; evaluate the supported Workflow
  interface before selecting the implementation API. Do not silently treat the
  October design's framework API assumptions as current.

## Run this bounded experiment

With the local `.venv` already installed, run:

    .\.venv\Scripts\python.exe -m unittest test_spike_persistence -v

This is a verified local experiment command, not fresh-clone application setup.
The lock is a Windows/Python-specific environment snapshot; a clean installation
from it has not yet been verified. The virtual environment's ensurepip bootstrap
failed; installation succeeded using the bundled Python's pip `--python` option.

## Outstanding gates

Selected model connection: Gemini API key stored locally. Copy `.env.example`
to `.env` and populate `GOOGLE_API_KEY`; the model can remain blank until account
availability is checked. `check_model_config.py` reports only configuration
presence and makes no network request. The key's presence does not prove validity.

Starting model selected: `gemini-3.8-flash`. Google's model documentation lists
it as stable with structured-output support (checked 30 October 2026):
https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash
The local configuration now contains a key and this model ID. The key has not
been displayed. `check_gemini_connection.py` makes one bounded, synthetic JSON
request; successful transport does not establish code-review quality or full
ADK/model compatibility. Record the reported model version in later evaluations.

Connection observation: two bounded synthetic requests on 30 October both
returned HTTP 504 (`ServerError`). API access and credential validity remain
unverified; do not attribute a gateway timeout to a bad key or model rejection.
Configuration checks report both key and model present. Both check scripts
passed Python compilation. Live model testing remains pending.

Fallback review: the user authorized 3.7 Flash as an alternative. Google's current
3.7 model page states that API calls to `gemini-3.7-flash` are automatically routed
to 3.8, so it is not an independent fallback for diagnosing 3.8 availability:
https://ai.google.dev/gemini-api/docs/models/gemini-3.7-flash
Keep the configured default at 3.8 rather than implying independent model coverage.
The 3.7-alias request also returned HTTP 504. This does not isolate whether the
failure is in local routing, an intermediary, or the upstream service.

After the user enabled billing on 30 October, the bounded Gemini check PASSED:
requested and reported model `gemini-3.8-flash`; response validated against the
ConnectionReply schema. No further account troubleshooting is currently needed.
This establishes direct SDK connectivity and basic structured output, not yet
four live ADK specialist reviews or review quality. The timing alone does not
prove billing was the cause of the earlier 504 responses.

Subsequent live integration PASSED: four real ADK reviewers using Gemini 3.8
Flash returned validated, source-linked findings; their invocation spans
overlapped. LangGraph persisted the result at a human interrupt, and an independent
process recovered an identical digest. See `LIVE-REVIEW-RESULT.md` for results,
two prior schema failures, compatibility adjustment and remaining limitations.
This supersedes the earlier pending-live-review status only; patch execution,
planning and full application acceptance remain outstanding.

Subsequent synthesis/classification prototype is implemented and verified:
`ACTION-CLASSIFICATION-RESULT.md`. Eight rule tests passed, a live ADK synthesis
call classified five actions from replayed review evidence, and a separate process
recovered the persisted plan. This supersedes the pending-planning status for
the bounded prototype only. The full intake/planning/patch workflow is not yet
integrated; exact-patch authorization and execution remain outstanding.

Live schema-validated model reviews and model pinning require a configured model
connection. Container execution requires Docker or another approved container
runtime. Authenticated Git cloning is required to restore history and normal
branch-based delivery. Exact-patch authorization, planning, execution, recovery
after APPLY, evaluations and the actual application remain unimplemented.
Never commit credentials.
