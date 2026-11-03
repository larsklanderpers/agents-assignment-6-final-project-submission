# Assignment 5 development pilot — 3 November 2026

This is additional work beyond the checkpointed rehearsal demonstration. It does
not replace the published original corpus scores or establish rubric completion.

## What was actually run

Pinned source: Assignment 5 commit `3ec39333b23cbcb67bbdd87bcec68fb2914029af`.
Three committed files were captured as a read-only review snapshot. A separate
development corpus uses the original output-filter helper as one control and two
explicitly seeded defects: omitted email masking and exposure of six account
digits instead of four. Neither defect was inserted into the original repository.

Corpus SHA256: `38f3314ad063f8eed8cb1e72679c512b955c12c0632e95540adee980839d663a`.
The source attribution, mutation descriptions, visible tests and hidden acceptance
tests are frozen in the private local manifest. Acceptance baseline: control
passes all twelve tests; each mutant passes three visible tests but fails the
relevant hidden tests. The three preflight expectations all matched.

| Development experiment | Case outcomes | TP / FP / FN | Precision | Recall |
|---|---:|---:|---:|---:|
| Pilot v1 | 3 / 3 | 2 / 2 / 0 | 0.50 | 1.00 |
| Pilot v2 | 3 / 3 | 2 / 0 / 0 | 1.00 | 1.00 |

Each pilot ran one repetition of the same three cases. Each left the control
unchanged and generated two source repairs, both passing twelve acceptance tests.
These are model-generated proposals, not supplied reference corrections. Cases
were counted successful only after independent isolated acceptance; abstention on
a defective case or a patch on the clean control would fail the complete-case
criterion. All assigned cases, failed reviews and failed operations are retained.

The first pilot's test-gap reviewer restated both security defects as test gaps,
including production-fix recommendations. The revised instruction requires an
actual missing-test claim. The filter also merges reports with identical path,
line and contract across specialists, keeping the raw duplicate reports. This
coarse rule can merge distinct issues at one location, so it needs broader testing.
Prompt and filter changes were evaluated together; this pilot does not isolate
their individual causal effects.

Every evaluated patch used a new, clearly simulated grant through the existing
ledger and persistent LangGraph gate. Wrong-mode and changed-patch consumption
checks rejected misuse. No actual human approval was claimed. No original
repository file, real rehearsal grant or historical operation was changed.

## Failures and limitations retained

Before the corpus pilots, the first three-file repository review was rejected for
multi-line/incorrectly indented source citations. All raw responses remain in
`artifacts/hardening/assignment5-review-v1/`. Explicit numbered source context
allowed v2 to pass exact-line validation. Its two test-coverage findings still
need human semantic review and are not claimed as independently confirmed bugs.

The pilot has two seeded defects in one already-inspected helper. It is a
development experiment tuned after v1 results, not a holdout, external benchmark
or broad repair-success estimate. Scores use provisional category/function
matching. No claim is made that original held-out precision rose from 0.411 to
1.00: these are different datasets and protocols. The original missed targets
remain part of the reflection.

The generated-patch path currently supports one source file and one planned step.
Both repairs succeeded on their first attempt, so model-driven recovery was not
exercised by these pilots. A second-attempt path exists but requires deliberate
failure trials. Live generic-repository approval/execution and GitHub PR intake
remain future milestones, as do independent holdout labels, multiple repetitions,
multi-file dependencies, and baseline comparisons under identical contracts.

## Verification and evidence

Full regression: 56 tests passed in 86.776 seconds. Five focused hardening tests
also passed after the duplicate-filter change. Read-only verification found no
changes among all 24,211 pre-dashboard archived evidence files. Assignment 5's
working tree remained clean.

Private local evidence (intentionally excluded from source packages):

- `artifacts/hardening/assignment5-intake-v1.json`
- `artifacts/hardening/assignment5-oracle-preflight-v1/`
- `artifacts/hardening/assignment5-e2e-pilot-v1/`
- `artifacts/hardening/assignment5-e2e-pilot-v2/`
- `artifacts/hardening/preserved-history-check.json`

Model inputs, raw outputs, token usage, plan, exact proposal, simulated grant,
checkpoint and Docker logs are retained under each attempted case. A source-only
clone needs an explicitly selected source repository to recreate the private
snapshot; it does not silently include Assignment 5 source or historical records.
