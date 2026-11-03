# Hardening phase — rehearsal paused

User requested rehearsal pause on 3 November 2026. No timer was started and no
new fault or repair decision was made. Resume only when Lars is ready after
reviewing the hardening work. Existing session records remain historical evidence.

Branch: `hardening/python-intake-evaluation`, from dashboard commit `237372d`.
Pre-dashboard baseline: `7bfe8ef`, tag `checkpoint/pre-dashboard-20261103`.
Verified and failed runs, private history archive, and Google Docs edits are
preserved. New development must use separate artifact directories.

Sequence: bounded committed Python intake; end-to-end generated-patch evaluation;
evidence-grounded reviewer precision, followed by independent measurements.

Assignment 5 is the user-approved development/integration source at commit
`3ec39333b23cbcb67bbdd87bcec68fb2914029af`. It is already inspected and cannot
serve as an unseen holdout. Start with pure Python guardrail helpers. Retain
source attribution and distinguish original code from deliberately seeded
defects. Do not change the original assignment repository or its test results.

The prior corpus and reported scores remain frozen. A fresh unseen holdout,
human label review, and full repeated measurements are required before claiming
generalization or the 0.80 precision/recall targets are achieved.

## First milestone observed

- Committed selection intake implemented and validated on three Assignment 5 files.
  Snapshot SHA256: `46f5f214248a217d501ca7dc79b6c4767550d3fa5c4d44d7a4b81b5a4b1df294`.
- Four-agent repository review v1 rejected inaccurate source citations; raw
  output retained. V2 passed citation validation after explicit numbered-line
  context; it proposes two test-coverage gaps, not independently verified defects.
- Three new development cases frozen before execution. Independent offline
  preflight passed their expected original/control and seeded-defect outcomes.
- End-to-end pilot v1: 3/3 complete-case outcomes; precision 0.50, recall 1.00.
  Duplicate cross-specialist reports explain the two provisional false positives.
- Pilot v2 after role clarification and location/contract deduplication: 3/3
  complete-case outcomes; precision 1.00, recall 1.00, only two labelled defects.
  Each generated repair passed 12 tests. These are one-repeat, tuned development
  measurements, not independent confirmation of the original held-out targets.
- Every patch operation in both pilots used a simulated ledger grant and a
  persistent LangGraph interrupt. Original Assignment 5 files were not changed.
- All 56 regression tests passed; the subsequent deduplication change also passed
  its five focused tests. All 24,211 pre-dashboard evidence files still match
  their checkpoint hashes. The Assignment 5 Git working tree remains clean.
- Google Docs reflection updated through a guarded append and readback verified.
  The primary recording remains baseline-focused; a secondary recording is
  conditional on verified completion and instructor submission rules.

See HARDENING.md for commands and HARDENING-RESULTS.md for interpretation.
Next: human-adjudicated labels and a new holdout; controlled repeated comparisons;
multi-file/dependent repair and forced recovery coverage; live repository patch
contracts and PR intake. Do not call those remaining milestones completed.
