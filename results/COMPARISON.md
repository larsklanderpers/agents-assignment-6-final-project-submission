# Parallel specialists versus single general reviewer

Frozen manifest `730e71e27e42ee349bf02185a608d4c2add52ac0f4d0c6507351ed01e1e3ad70`, seed 505. Six development fixtures, six renamed held-out variants, four clean controls; three repeats each. There are 16 fixtures, not 48 independent fixtures per mode. Labels were frozen before evaluation and were not tuned.

| Measure | Parallel specialists | Single reviewer |
|---|---:|---:|
| completed | 48.000 | 48.000 |
| failed | 0.000 | 0.000 |
| actual_call_responses_with_usage | 192.000 | 48.000 |
| held_out_macro_precision | 0.411 | 0.510 |
| held_out_macro_recall | 1.000 | 1.000 |
| control_unmatched_findings | 31.000 | 15.000 |
| p50_seconds | 9.852 | 6.406 |
| p95_seconds | 15.750 | 15.110 |
| total_active_seconds | 500.860 | 351.767 |
| prompt_token_count | 49956 | 11793 |
| candidates_token_count | 29391 | 20360 |
| thoughts_token_count | 22361 | 2792 |
| total_token_count | 101708 | 34945 |

The single reviewer produced fewer unmatched findings and used fewer calls on this tiny corpus. Both modes missed the >=0.80 held-out precision target. Neither result supports a claim that four specialists improve accuracy. All 96 attempts completed without dropped runs or retries.

Scores are provisional automatic category/symbol matches after exact source-line validation. Matching does not prove a finding is substantively correct. Sparse frozen labels may omit valid discoveries; all unmatched and duplicate findings count as FP in the original score. Human label review and blinded semantic adjudication remain pending; any amended score must be published alongside this original score. Clean-control alerts (especially test coverage/style) show over-reporting under the frozen rubric and require inspection.

The model and temperature are identical. Each mode has an aggregate 8192 output-token ceiling per snapshot; specialists have four calls and separate role prompts, the baseline has one call and a combined prompt. Actual token usage differs; this is a matched maximum-output-budget comparison, not a matched monetary-cost experiment. Token metadata includes provider-reported thinking where supplied. Missing counts are not invented; no monetary estimate is available.

Raw synthetic responses, source-linked evidence, spans, usage and per-run counts are included in each mode directory. metadata.json records environment, model alias, lock/prompt/harness hashes and the design-base Git revision. Source was locally uncommitted during execution; do not mistake the design-base revision for a commit containing the implementation. Original raw outputs remain under ignored artifacts/evaluation/. Reporting/packaging code was refined while the first run was in progress; the recorded invocation hashes identify the code used at launch.

## Coverage and denominators

- Live corpus reviews: 96 attempts, 96 complete; 192 specialist calls and 48 general-reviewer calls.
- Authored corpus oracle verification: 16/16 original/corrected contract pairs; 32 container runs. Original SQL/tenant vulnerabilities intentionally fail hidden regression assertions; their corrected variants pass.
- Authored test usefulness: 2/2 seeded mutants detected in two test-gap fixtures, using two additional container runs. These are harness-authored tests, not agent-authored test success.
- Agent corpus patch attempts: 0. Accepted-patch behavior preservation, corpus approval integrity, corpus mutation trace completeness, corpus recovery and per-complete-case repair success are N/A.
- Dependency/conflict fixture findings are evaluated; no corpus planning/DAG quality score or fixed-order non-replanning baseline is available. Separate planning and safety tests do not fill those denominators.
- Original four human-approved operations and regression simulations remain separate evidence; there was no corpus approval simulator because no corpus edits were attempted.

No held-out acceptance target, production safety certification or general performance speedup is claimed.
