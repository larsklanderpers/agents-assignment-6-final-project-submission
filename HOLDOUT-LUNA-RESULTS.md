# Blinded Luna-authored holdout — 4 November 2026

This is a separately authored, blinded holdout evaluation of a frozen
Gemini-based review system, using Luna-generated cases and labels. Executable
original/reference checks established consistency for the intended labels;
independent human adjudication and label-completeness review remain pending.
It measures review accuracy, not generated-repair success or general PR intake.

## Freeze and separation

- Frozen implementation: `6d3b31496ae9efe3047168e81bc0d95c9a6a7c26`, tag
  `holdout/frozen-gemini-20261104`. A separate 242-file source snapshot was hashed
  before case authorship and checked before/after review and before scoring.
- Reviewer: configured model alias `gemini-3.8-flash`, temperature 0, low thinking,
  maximum 4,000 output tokens per specialist, four specialists, one run per case.
  This pins application configuration, not the provider's underlying weights.
- Author: `gpt-6-luna`, separate agent with a fresh context. It received a task
  specification and package schema, but no implementation, prior prompts,
  examples, findings or scores. Different models can still share blind spots.
- Twelve original synthetic Python cases: eight labelled defects (two per
  category) and four intended clean controls. Files use opaque case IDs.
- Public inputs contain only source, visible tests and explicit contracts.
  Labels, corrected reference files and private checks reside separately.
  The tool-free Gemini model received only the public payloads; all twelve
  serialized inputs were checked against that package with no mismatches.
- This is model-input separation, not an OS-level confidentiality boundary.
  The local evaluator can access private files. No claim is made that synthetic
  patterns could never have appeared in either model's pretraining.

Public package SHA256:
`ec1a229a1f69433ca5f033dde470bae198deead1fd502ba6145d5eb36a6aad69`.
Final private package SHA256:
`e6c420b9ee36faf31e8a4ca7d5a658f78d283725c7d991b8924a58d9ff1c96b5`.

## Checks before evaluation

The first private preflight stopped on a missing reference-file content field.
Luna preserved the exact draft and corrected that field; public inputs were
unchanged. No Gemini outputs existed at that point. The next preflight ran all
original/reference pairs in the pinned offline Docker runner: all twelve matched
the expected oracle behavior. No cases were excluded. These checks establish
that intended defects are detectable, not that the key lists every valid finding.

The final packages were sealed before any reviewer calls. The scoring procedure
was recorded in advance: one-to-one category/path/top-level-function matching;
duplicate or unmatched defect findings count as provisional false positives;
failed reviews retain their labels as false negatives. Raw defect proposals and
filtered accepted defects are reported separately. Suggestions/hypotheses are not
counted as defect predictions. Missing precision denominators would be N/A.

## Locked results against Luna's original key

All twelve reviews completed, with no retries or evaluation-driven prompt
changes. Forty-nine output files were hash-locked before scoring. The 48 provider
responses reported 42,251 total tokens. Summed active review time was 99.953
seconds; monetary cost was not calibrated.

| Output | Matched findings | Unmatched findings | Missed labels | Micro precision | Macro precision | Recall |
|---|---:|---:|---:|---:|---:|---:|
| Raw defect proposals | 8 | 5 | 0 | 0.615 | 0.821 | 1.000 |
| Filtered accepted defects | 8 | 3 | 0 | 0.727 | 0.850 | 1.000 |

Micro precision weights all findings equally; macro precision gives each review
category equal weight. Both micro and macro recall were 1.000. Reporting only
the macro result would conceal the weaker test-gap category.

| Filtered category | TP | Provisional FP | FN | Precision | Recall |
|---|---:|---:|---:|---:|---:|
| Security | 2 | 0 | 0 | 1.000 | 1.000 |
| Performance | 2 | 0 | 0 | 1.000 | 1.000 |
| Style | 2 | 0 | 0 | 1.000 | 1.000 |
| Test gaps | 2 | 3 | 0 | 0.400 | 1.000 |

Three of the four intended clean controls received no accepted defect findings.
Filtered findings exactly matched the original key on 9/12 cases; raw findings
did so on 8/12. These are exact review outcomes, not repair-success rates.

## Post-score diagnostic: the key is incomplete

The three filtered unmatched findings concerned absent tests for tenant mismatch,
inactive publishing membership and disabled editing accounts. Inspection after
output locking showed those requirements in the public contracts but not exercised
by the visible tests. A separate offline diagnostic supported all three gaps:

- For case-01, a disposable tenant-check mutant passed the visible suite but failed
  the targeted tenant-isolation check. This case was labelled a clean control.
- For case-05, the unchanged defective source passed visible tests but failed the
  newly added inactive-publisher check.
- For case-10, the unchanged defective source passed visible tests but failed the
  newly added disabled-owner check.

These are post-score, coordinator-authored diagnostics, not new holdout outcomes
or independent human judgments. They support the coverage findings and expose
incomplete author labels. The original key, outputs and scores remain unchanged;
no post-hoc perfect score is substituted. Independent human adjudication should
review both the unmatched findings and the semantic validity of all matches.

The numerical macro target of 0.80 was exceeded against this key, while overall
micro precision was below 0.80. Given the incomplete labels, small synthetic
sample and one repetition, neither should be presented as settled system accuracy
or proof that precision is fixed. The old 0.411 development-era held-out result
remains intact; the datasets and protocols are not a controlled before/after
comparison. This set must not be reused as unseen validation after tuning on it.

## Preservation and recording scope

The baseline rehearsal remains paused, with no new human approval consumed.
Existing verified/failed runs and prior evaluation results are preserved. The
primary recording follows the established rubric-focused baseline. This holdout
is additional evidence; a second recording remains conditional on verified scope
and the instructor's submission rules. It does not resolve live general-repository
execution, PR retrieval or broader end-to-end repair evaluation.

All private evidence is under `artifacts/holdout-luna-20261104/`, excluded from
Git/source packages: freeze/protocol, author packages and draft, preflight records,
package lock, reviewer outputs and lock, input audit, scores and post-score checks.
The public summary in `results/holdout-luna-20261104/summary.json` contains aggregate
metrics only. No answer key is included there.

The new runner/scorer boundary tests passed (five tests). No frozen reviewer code
was changed to accommodate these cases or their outcomes.
Final hash checks matched all 24,211 earlier evidence files, all 242 frozen source
files, both preregistered runner/test files and all 49 locked reviewer output files.
