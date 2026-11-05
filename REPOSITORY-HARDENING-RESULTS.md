# Repository intake and broader repair evaluation — 4 November 2026

This is additional work on `hardening/python-intake-evaluation`. The original
rubric demonstration remains paused, its characterization approval remains
VERIFIED, and its deliberate fault still awaits the timed personal decision.
Nothing here approves or modifies that run.

## What now works

- Public GitHub PR URLs are fetched into new bare repositories without checkout,
  hooks, dependency installation, pushes or merges. Exact base/head commits and
  selected-file hashes are recorded. PR changes during intake are rejected.
- Local committed Python selections can pass through review, planning, proposed
  repair, a persistent terminal approval gate and isolated Docker verification.
- Plans support up to three dependent steps, each changing up to four existing
  production files. Every live step requires its own exact personal approval.
  Failed proposals retain their original parent and quarantined export; a retry
  is a new candidate. Interrupted ambiguous operations cannot silently replay.
- The broader workflow adds a correctness specialist to the existing four
  reviewers. The original reviewer and frozen Luna/Gemini holdout are unchanged.
- Successful output is a verified export and exact diff. Original checkouts are
  never edited. Publishing a patch or merging a PR remains a separate action.

## Observed end-to-end results

Four synthetic development cases were frozen before execution and run twice:
clean multi-module code, a discount defect, two defects across dependent modules,
and a repair with a deliberately injected failed proposal. Each repair case has
two visible tests and six private acceptance tests. Private assertions are not
sent to the model; recovery receives actual counts and the failed proposal.

| Measure | Four-reviewer v1 | Five-reviewer v2 |
|---|---:|---:|
| Complete case outcomes | 2/8 (25%) | 8/8 (100%) |
| Repair cases resolved | 0/6 | 6/6 |
| Clean controls preserved | 2/2 | 2/2 |
| Forced-failure recovery demonstrated | 0/2 | 2/2 |
| Unchanged baseline passes acceptance | 2/8 | 2/8 |

V1 revealed a real scope gap: none of the original four specialist categories
owned ordinary arithmetic correctness. V2 adds that responsibility explicitly.
Both two-module runs used two dependent repair steps. The intermediate step
passed visible regression tests; the final step and a separate final check
passed all eight tests. Intermediate VERIFIED means the specified step's checks
passed, not that every remaining plan defect was already fixed.

The failed proposals in the recovery cases were deliberately inserted by the
harness, after preserving the model's original proposal. They are not reported
as spontaneous Gemini failures. Each was quarantined; a fresh generated attempt
from the unchanged step parent passed. All benchmark approvals were simulated.

This is a tuned development comparison on four related synthetic cases with two
repeats, not eight independent problems, an unseen holdout, or a production
success estimate. It measures complete repair outcomes, not precision/recall.
It does not replace the original or adjudicated Luna review scores. It uses
stdlib unittest with no third-party installation; broader ecosystems, hostile
test programs and arbitrary repository setup are outside the demonstrated scope.

## Real intake evidence and pending personal approval

Assignment 5 PR #1 was successfully retrieved from GitHub:
`https://github.com/larsklanderpers/agents-assignment-5/pull/1`.
Base `9d40ee4b032ab31abebefe39faab6242f770a893`; head
`3ec39333b23cbcb67bbdd87bcec68fb2914029af`. All changed filenames were recorded;
three selected guardrail source/test files were frozen. Those selected files
are context, not a claim that all changed PR files were reviewed. The PR is
already merged/closed: historical inspection is supported, live approval is
rejected. Open-PR movement/closure rejection is covered by controlled tests;
no real open PR has yet completed a personal repair approval.

A new disposable, committed Assignment 5 development copy contains the clearly
labelled seeded email-redaction omission. Its visible three-test baseline passes.
The five-reviewer workflow prepared the exact repair: remove the email-skipping
condition. The live candidate is awaiting personal approval with zero decisions
and zero operations. A separate simulated preflight passed all twelve tests
in the existing development acceptance suite for the same proposal. This does
not consume or stand in for personal approval.

Live candidate:
`artifacts/hardening/assignment5-local-repair-20261104-v1/preparation/candidate`.
This is additional development evidence, not the prepared rehearsal run.

## Validation and preservation

- Full regression suite: 68 tests passed in 81.962 seconds.
- After adding three more rejection tests: all ten focused repository tests passed.
- Checks cover wrong approval mode, tampered bundle/diff, unmet dependencies,
  protected tests, stale local source, changed/closed PRs, a PR-fetch race,
  noninteractive approval rejection, quarantined failure and interrupted replay.
- All 24,211 pre-dashboard evidence files match their recorded hashes.
- Original Assignment 5 checkout, original holdout outputs and answer key remain
  unchanged. Existing Google Docs text is preserved by a guarded append.
- Every evaluation output, failure, proposal, ledger and test log remains in its
  separate artifact directory. Executed source copies match protocol hashes.

Evidence: `artifacts/hardening/repository-e2e-20261104-v1/` and `-v2/`,
`assignment5-pr-intake-20261104-v1/`, `assignment5-local-repair-20261104-v1/`,
`repository-regression-20261104.log`, `repository-focused-20261104.log`, and
`repository-preservation-20261104.json`. Portable summaries are under
`results/repository-hardening-20261104/`.

## Remaining boundaries

The implemented intake supports bounded public GitHub PRs and local committed
Python selections; it is not a general private-host/multi-language importer.
Selections must include enough dependencies and discoverable stdlib tests.
The Git download is time-limited, while selected source/export sizes are bounded;
large repositories may still require a more restrictive download strategy.
Original third-party test harnesses are not converted automatically. Live
multi-step continuation exists but has not yet been exercised with personal
approvals. The dashboard still presents the established demonstration evidence;
the new experimental report is separate. A fresh independent repair corpus and
larger repeated study would be required for broader reliability claims.

See REPOSITORY-WORKFLOW.md for commands. Review/edit the reflection and complete
the established rehearsal/recording before describing these additions as a
second completed submission attempt.

## Personal verification — 5 November follow-up
The earlier pending personal approval status is superseded by recorded operation
4354e13524e14850b253dcc5dbd6c0f3: VERIFIED, interactive approval by LARSKLANDER,
three visible tests passed. This is the deliberately seeded disposable local
Assignment 5 copy, not a live PR repair. The separate 12-test simulated preflight
is additional test evidence, not human permission. Original results above remain
unchanged. The reflection and dashboard distinguish these evidence categories.
