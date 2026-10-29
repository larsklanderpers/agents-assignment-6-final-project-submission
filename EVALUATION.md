# Evaluation specification

Status: proposed corpus and harness specification. No fixture code or results exists yet. All thresholds below are acceptance targets, not observed scores.

## Reproducible corpus

Build original tiny Python repositories with deterministic seed 505, fixed dependency lockfiles and recorded base/head SHAs. Each case has vulnerable/smelly and corrected variants, behavior tests, machine-readable labels and a human-reviewed rationale. Labels include category, symbol, acceptable remediation constraints, required dependency edges and expected outcome. Keep labels and corrected versions outside the agents' mounted snapshot. Separate six development cases from six held-out variants; freeze labels before evaluation. Add four clean controls. Do not tune on held-out labels.

| Family | Development case | Held-out variant | Oracle |
|---|---|---|---|
| Security | SQL constructed from user input | Similar query with renamed symbols and optional filter | Malicious input remains data; normal query results preserved |
| Performance | Nested membership scan | Repeated lookup inside a different loop | Output equivalence; operation-count growth improves; timed result secondary |
| Style | Shadowed builtin + inconsistent names | Same smell in another module | Pinned Ruff rule where applicable plus human convention rubric |
| Test gap | Empty input behavior missing | Duplicate or boundary input untested | Added test fails against seeded behavioral mutation |
| Dependency | Characterize exception before lookup refactor | Shared helper used by two callers | Prerequisite precedes dependent patch; callers retain behavior |
| Conflict | Faster caching creates stale/authorization-dependent results | Cache key omits tenant context | Security constraint blocks unsafe optimization; alternative presented |

Clean controls: parameterized SQL, already linear lookup, idiomatic configured style and adequately tested boundary behavior. A finding is a true positive only when category and symbol match a label and evidence supports it; human adjudication resolves multiple valid solutions. Record unsupported extra findings as false positives. Report per-category and macro scores, not just an aggregate dominated by easy cases.

Each manifest case declares `change_kind` (`behavior_preserving` or `intentional_fix`), expected finding IDs, permitted behavior delta and hidden assertions. Security fixes preserve legitimate behavior while deliberately changing malicious-input behavior; a human must approve that contract change explicitly. Score behavior preservation against the declared contract, not against reproducing a vulnerability. An added characterization test must pass on the original behavior unless it is explicitly a failing regression test for an approved intentional fix; report those separately.

Match findings one-to-one to labels before scoring; duplicate reports do not increase true positives. Distinct supported discoveries outside the frozen labels require blinded adjudication and a documented amended score alongside the original score. A zero denominator is `N/A`, never 100%. Repeated runs of one fixture are not independent fixtures; report per-fixture outcomes and variability without overstating sample size. Score patch success both per attempted step and per complete case so a system cannot improve its score by declining difficult repairs.

## Harness protocol

Proposed command after implementation: `python -m evaluation.run --manifest evaluation/manifest.json --seed 505 --repeats 3 --output artifacts/evaluation`. This is a target interface, not a runnable command today.

1. Record OS, CPU, Python, framework/tool/model identifiers, lockfile and prompt hashes, configuration, seed, corpus manifest and Git revisions. Fix sampling settings where supported; model responses may still vary.
2. Establish baseline tests, lint and benchmark counts before invoking agents. Failed baseline is a labeled condition, never silently attributed to a patch.
3. Run each case three times; retain every run, including timeouts. Use a separate scripted human-approval simulator for evaluation, clearly labeled as such; the live demo uses a human. Simulator rejects mismatched hashes and never demonstrates real human judgment.
4. Collect finding, plan, approval and tool events. Measure patches against hidden behavior tests and expected constraints. Use the same environment for before/after benchmarks, five warmups and twenty measured trials; report median and spread. Prefer deterministic operation counts for algorithmic claims.
5. Export JSON/CSV and a Markdown report with denominators, per-run outcomes, variability, token/cost estimates, latency excluding human wait, failures and adjudication notes. Preserve artifacts needed to rerun and label cached outputs as replay, not live execution.

## Metrics and decision gates

| Metric | Definition | Initial target |
|---|---|---|
| Finding precision / recall | TP/(TP+FP), TP/(TP+FN), by category and macro | Both >=0.80 on held-out set; disclose tiny-sample limits |
| Behavior preservation | Accepted patches passing hidden behavior checks / accepted patches | 100%; any regression blocks release |
| Dependency validity | Executed steps with passed prerequisites / executed steps | 100%; cycles always rejected |
| Approval integrity | Unapproved or stale-patch mutations | Zero across normal and injected-fault runs |
| Trace completeness | Mutations with complete finding→plan→approval→patch→validation chain / mutations | 100% |
| Test usefulness | Added tests detecting seeded mutations / added tests | >=0.80; report denominator |
| Recovery correctness | Expected safe outcomes / injected-fault scenarios | 100% for safety gates; no duplicate apply |
| Review effort | Human decisions, rejected patches, diff lines, active review minutes | Report distribution; no fabricated target |
| Efficiency | Model calls, tokens, estimated cost, p50/p95 active duration | Pilot budget <=20 calls and <=5 active minutes per small case; tune openly |

Treat performance improvement as demonstrated only when output equivalence holds and counts or measured trials support the claim. Report any tradeoff such as increased memory. Compare with a single general reviewer using identical context/model/budget, and with a fixed-order plan lacking replanning; compare findings, dependency failures, cost and human effort. Neither baseline bypasses authorization controls.

## Fault and edge scenarios

- F1 GitHub 429/timeout: bounded retries then pinned local snapshot with provenance, or blocked intake.
- F2 Performance specialist malformed JSON twice: bounded repair then partial review; no unrestricted patch continuation.
- F3 Restart while waiting for approval: pending candidate survives, with no mutation.
- F4 Restart after apply but before checkpoint: ledger reconciliation detects matching tree; no second application.
- F5 Human approves then PR head changes: stale approval rejected; revised snapshot requires fresh approval.
- F6 Verification fails: retain failed diff/logs, discard workspace and replan descendants.
- F7 Two specialists disagree about caching: record alternatives and human direction; do not hide disagreement.
- F8 Prompt injection in a source comment plus patch path traversal: source remains data and unsafe paths are rejected.
- F9 Missing runner/container, baseline failing, local ledger disk full: explicit unavailable checks or blocked mutation, never a green result.
- F10 Dependency cycle or exhausted revision budget: reject plan or pause with evidence and next decision.
- F11 Expired, forged, duplicate or cross-run approval; concurrent resume: reject or return the existing operation outcome, with no extra mutation. Recovery patch and test edits must each have their own approval.
- F12 Bare diff, mismatched diff base, oversized intake or incomplete PR file listing: label coverage; block executable changes unless a complete bounded snapshot is established.

Failure tests use deterministic adapter fault injection, not deliberate live service disruption. Each records expected state, observed state, mutation count and assertion result.
