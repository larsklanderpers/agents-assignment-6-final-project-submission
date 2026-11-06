# Frozen corpus finding evaluation

Manifest SHA256: `730e71e27e42ee349bf02185a608d4c2add52ac0f4d0c6507351ed01e1e3ad70`. Seed 505. 48 runs; 16 fixtures.

These are automatic category/symbol matches with exact source-line validation, pending semantic human adjudication.

| Split | Category | TP | FP | FN | Precision | Recall |
|---|---|---:|---:|---:|---:|---:|
| development | security | 6 | 0 | 0 | 1.000 | 1.000 |
| development | performance | 3 | 6 | 0 | 0.333 | 1.000 |
| development | style | 3 | 8 | 0 | 0.273 | 1.000 |
| development | test_gap | 6 | 12 | 0 | 0.333 | 1.000 |

development: 6 fixtures, 18 runs, 0 failed. Macro precision 0.485, recall 1.000.

| Split | Category | TP | FP | FN | Precision | Recall |
|---|---|---:|---:|---:|---:|---:|
| held_out | security | 6 | 0 | 0 | 1.000 | 1.000 |
| held_out | performance | 3 | 6 | 0 | 0.333 | 1.000 |
| held_out | style | 3 | 5 | 0 | 0.375 | 1.000 |
| held_out | test_gap | 6 | 12 | 0 | 0.333 | 1.000 |

held_out: 6 fixtures, 18 runs, 0 failed. Macro precision 0.510, recall 1.000.

| Split | Category | TP | FP | FN | Precision | Recall |
|---|---|---:|---:|---:|---:|---:|
| control | security | 0 | 0 | 0 | N/A | N/A |
| control | performance | 0 | 0 | 0 | N/A | N/A |
| control | style | 0 | 3 | 0 | 0.000 | N/A |
| control | test_gap | 0 | 12 | 0 | 0.000 | N/A |

control: 4 fixtures, 12 runs, 0 failed. Macro precision 0.000, recall N/A.

Active review latency p50: 6.406s; p95 nearest rank: 15.110s.

All attempts and failures are in runs.jsonl; no automatic retries or dropped repeats. Mode: single. Complete parallel reviews use four calls; single-reviewer baseline uses one call with the same 8192 aggregate output-token limit. Token metadata is retained per response; monetary cost is unknown.

## Limits

- Category/symbol matching is automatic; semantic evidence adjudication pending.
- Labels are original machine-authored, frozen before evaluation; independent human label review pending.
- Held-out variants are small renamed variants, not an independent external dataset.
- No corpus patch/planning/baseline comparison is measured; behavior and approval metrics N/A.
- Dependency/conflict are fixture families scored by test_gap/security finding category only.
- No calibrated pricing: cost unknown; failures may incur unreported provider usage.

No acceptance target is claimed met from these provisional scores. Frozen labels were not modified after seeing outputs. Unsupported or duplicate category/symbol matches count as FP; missing outputs count as FN. Zero denominators are N/A.

Corpus patch attempts: 0. Behavior preservation, mutation-test usefulness, trace completeness for corpus mutations and corpus recovery: N/A. See separate verified human operations and safety regression tests; those are not corpus outcomes.

Publication note: table formatting repaired; raw report retained locally. The single-reviewer comparison is in ../COMPARISON.md; original run metadata limits are preserved verbatim.
