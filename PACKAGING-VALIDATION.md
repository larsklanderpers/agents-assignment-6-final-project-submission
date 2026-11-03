# Packaging and execution validation — 2 November 2026

Local implementation branch: `implementation/first-patch`; design-base commit
`4c4ca01`. Source is locally modified/uncommitted. No implementation push, merge,
deployment or instructor-access check has been performed.

## Passed checks

- Python 3.12.14, ADK 2.13.0, LangGraph 1.2.18 and SQLite checkpointer 3.1.2.
- Source-only ZIP export excludes `.env`, `.venv`, `.git`, `artifacts/` and all
  historical ignored evidence. A SHA256 manifest accompanies the source.
- A new environment installed every pinned requirement without copying the
  development environment. Bootstrap pip's `--python` route avoids the known
  ensurepip limitation. `pip check`: no broken requirements.
- An actual local source-only Git repository was committed and cloned without
  hardlinks. Windows checkout initially changed corpus bytes; `.gitattributes`
  now fixes LF line endings. The final source validator checks every exported
  file and the frozen corpus digest after Git checkout.
- The original 32-test combined suite passed in 63.040 seconds, including real
  Docker isolation probes and separate-process persistence. New regression
  coverage additionally checks long operation paths and interleaved container
  output with duplicate-marker rejection; final combined suite passed 34 tests in 46.148 seconds in development and
  passed from the final source-only clone in 50.047 seconds (including startup).
- Original four historical operation bindings and baseline/candidate log hashes
  still match. `saved_evidence.py` reads those ledgers in SQLite read-only mode;
  it does not rerun their operations or re-certify workspace trees.
- Frozen corpus: 96/96 live finding reviews; 16/16 original/corrected oracle
  contracts plus 2/2 authored mutant detections. See `results/COMPARISON.md`.

## Fresh human rehearsal: actual failure and correction

`packaging-rehearsal-20261102` generated fresh four-agent review evidence,
live synthesis and a live test proposal with patch SHA256
`e2a9c4f3541ff40573cedc4f1276d688ca75946f76073e1ec2b349c97b1f395e`.

Lars personally approved it in the interactive terminal. Decision
`212fc5a7b14a450f8d7d6be78624d94b` was consumed by operation
`728750cb5b444beda6a05698bbe0e1ee`. Its zero-test baseline completed as
`no_tests`. The patch applied, but nested Windows paths hid the test file from
the Python workspace enumeration. The executor conservatively recorded
**AMBIGUOUS** and quarantined the workspace, without claiming verification.
The original ledger, checkpoint, baseline log and approved bytes are preserved.

The correction gives new operations short UUID workspace paths under
`artifacts/ws/<operation-id>/`. Each operation's `workspace-location.json`
declares the layout; readers derive and validate that exact location. Long
operation log paths use Win32 extended paths. Git receives its supported path
syntax, and historical workspace layouts remain readable. No symlinks, mounts
or credentials are introduced. UUIDs avoid collisions across runs.

A separately **simulated** approval fixture then completed real Git apply,
seven real tests in Docker and duplicate replay without an extra operation.
Its operation evidence path exceeded 260 characters. This test exposed a second
issue: Docker can interleave a result marker into a partial stderr progress
line. Parsing now accepts that ordering, requires one marker, validates counts
and rejects duplicate/spoofed markers. Sandbox policy and bootstrap are unchanged.

The replacement `candidate-93a15f976a12-exec-d24e41f5` received another real
human approval and completed Docker verification: FAILED, seven tests with one
incorrect expected ordering in the model-generated test. Operation:
`7e83013f61a549dd98bb5ebee2ffc7e6`. Its failure and quarantine are preserved.

The corrected expectation changes only `[1, 1, 1, 3]` to `[1, 1, 3, 1]`.
A new static literal-example check rejects the wrong order before gate preparation.
The exact corrected tests then passed 7/7 in a separately simulated Git/Docker
fixture before new candidate `candidate-32a6e3d26914-exec-v1` was prepared.
Both prior attempts' 79 evidence files remain byte-identical. See
[correction and verification](TEST-EXPECTATION-CORRECTION.md). The earlier clean-clone
proof below predates this static-check addition; its 34-test result is retained
as historical evidence, while the updated regression result is recorded separately.

## Final source-only clone proof

Snapshot archive: `artifacts/packaging/review-ledger-source-20261102.zip`, SHA256
`b65347533e7c025659e35ac02ac533cf7cfdb966089f7dbf6fe5c8f310f93b6e`.
Disposable local snapshot commit: `3af44f6`; actual clone: `artifacts/c3/`.
This is a packaging snapshot commit, not a commit in the working repository.
A documentation/result update is exported separately as the final delivery ZIP;
runtime source and lockfile are unchanged from this tested snapshot.

| Check | Exit/result | Elapsed seconds |
|---|---|---:|
| All 211 exported file hashes + corpus hash after Git checkout | pass | 2.750 |
| Unconfigured doctor | expected exit 1; key/model absent, Docker present | 5.218 |
| Combined 34-test regression suite | pass | 50.047 |
| Historical saved evidence absent in clean clone | honestly reported absent | 0.235 |
| Create unique run | pass | 0.250 |
| Fresh four-agent review | complete, overlap true | 14.906 |
| Fresh synthesis | validated plan at pending gate | 17.437 |
| Fresh test proposal + executor preparation | pending human gate | 20.047 |
| Read-only status | zero operations in clean-clone run | 0.266 |

The new/review/plan/propose/status route totals **52.906 seconds**. This includes
command startup and actual model/tool work, excludes human decisions and spoken
presentation, and is not a complete demo timing. API configuration was inherited
only in the proof process from the existing local `.env`; it was never copied
into the clone, source archive or result log. The clean clone used the independent
pinned environment installed in `fresh-clone-2/`, not the development environment.
This deliberately separates exact-source checkout verification from a repeated
install of the identical lock. The clean lock installation itself passed.

## Proof locations and limits

- Initial source archive / clean install: `artifacts/packaging/review-ledger-candidate.zip`,
  `clean-source-1/`; local clean clone iterations `fresh-clone-1/`, `fresh-clone-2/`.
- Locked clean-clone install log: `artifacts/packaging/fresh-clone-2-install.log`
  (`No broken requirements found`). This environment contains no copied key.
- Regression logs: `artifacts/packaging/regression-final.log`,
  `longpath-regression*.log`. Failed diagnostic attempts remain retained and are
  not counted as passes. Last standalone long-path regression: 1 passed in 7.637s.
- Final source archive, clone hash check, complete regression results and fresh
  clone-to-gate proof: complete in `artifacts/packaging/final-proof.json`; published summary in
  `results/packaging/proof.json`.

This is a local source-only clone proof, not a claim that the remote currently
contains implementation. The pinned requirements are a package-version snapshot
without distribution hashes; Windows/Python 3.12 is the tested platform. Final
docs/results may postdate the clean environment installation, but use the same
lockfile. The final source is exercised against that independently installed
environment. The fresh human-approved failure/replan/repair chain subsequently reached
VERIFIED and its saved evidence was audited. A full spoken <=10-minute
rehearsal/recording remains unmeasured.

Publication, instructor access, human corpus adjudication, corpus repair metrics,
typeset page counts, Canvas deadline confirmation and final recording remain open.

## Latest correction regression

After the expectation correction and static guard, the complete suite passed
**39 tests in 48.219 seconds**. Exact corrected tests passed 7/7 in the independent
simulated preapproval run. All 79 files from both earlier human attempts and their
quarantined workspaces remained byte-identical. The prior 34-test clone proof is
historical; no repeated install or new model review is claimed for this correction.
Updated source is exported as `review-ledger-delivery-20261102-r2.zip`, with its
file manifest and frozen-corpus hash checked after extraction.

## Fresh verified parent and optimization preparation

Corrected tests subsequently reached real human-approved VERIFIED (seven passes).
The trusted-harness path fix passed the complete 40-test suite in 52.223 seconds.
A separate simulated optimization preflight passed seven tests plus thirteen
checks before the next human gate was presented. See FRESH-REHEARSAL-RESULT.md.
The r3 delivery archive includes these current source/documentation changes;
older archives and clone evidence remain retained.

## Completed fresh chain and audit - 3 November

The real repair reached VERIFIED, seven tests plus thirteen checks. Read-only
audit checked the four stages' approval/manifest/operation bindings, consumed
interactive decisions, both log hashes, terminal checkpoints and actual files
against recorded trees. Core evidence files were unchanged by the audit; the
prior failed attempts' 79 files remain unchanged. Follow-up is eligible only for
proposal and remains unauthorized/unexecuted. See FRESH-REHEARSAL-RESULT.md.
Latest implementation regression remains 42 passed; no approved operation was
rerun for this audit. Final documents and the delivery package are refreshed
separately from the preserved run artifacts.
