# Live four-reviewer integration — 30 October 2026

Result: PASS for the bounded ADK/LangGraph integration experiment. This is not
the completed refactoring application or a corpus evaluation.

Run: `live-20261030-3`; model requested: `gemini-3.8-flash`.
Four real ADK LlmAgents reviewed the same original ten-line Python source as
text. No reviewed code was executed, and no patches were proposed or applied.

| Specialist | Findings | Observed output |
|---|---:|---|
| Security | 1 | SQL constructed by concatenating user input; parameterization recommended |
| Performance | 1 | Repeated membership lookup could be quadratic for sequence inputs |
| Style | 1 | Function naming convention and shadowed `list` builtin |
| Test gap | 2 | Missing supplied evidence for query tests and collection boundary tests |

All four results passed strict local Pydantic validation, unique author/agent
matching, category matching and exact line-number/source-text checks. Those
checks establish structural validity and source linkage, not semantic correctness.
The shared interval across measured ADK invocation spans was approximately 4.83
seconds; total review span approximately 10.58 seconds. These are client agent
execution spans, not proof of simultaneous inference inside Google's service.

LangGraph stored the complete result and paused at a review-only human interrupt.
A separate `inspect` process recovered the pending gate and identical result
digest without making model calls:

    3c8c40e4c587a63bb6c40f0d34d690bad15f95f4d748b01ad670235dfe2322c3

Local raw evidence: `artifacts/live-spike/result.json` and SQLite checkpoint in
that directory (ignored by Git). Re-run inspection using:

    .\.venv\Scripts\python.exe spike_live.py inspect --run live-20261030-3

## Compatibility finding

Two earlier attempts failed with HTTP 400 because the provider schema contained
`additional_properties`. ADK 2.13's schema transport does not accept the strict
Pydantic extra-field setting. The provider-facing schema now omits that setting;
returned JSON still passes the separate strict local Review schema, which
rejects extra fields. Both failures stopped before the decision gate. They were
configuration debugging attempts, not successful reviews or fault-suite scores.

ParallelAgent remains deprecated in ADK 2.13. This experiment proves the pinned
interface works; implementation API migration remains an explicit task.

## Review limitations and next gate

No repository test suite or style configuration was supplied. Test-gap results
mean evidence was absent from the input, not that an actual repository lacks
tests. The performance suggestion needs characterization tests for duplicates,
ordering and unhashable inputs before any set-based change. The SQL fix must
use the actual driver's parameter syntax. No benchmark or security exploit ran.

Next: planner synthesis and a validated dependency DAG, followed by patch proposal
and exact-patch human authorization. This experiment's gate cannot authorize
execution. Container support, operation-ledger crash recovery, final model
version reporting, token/cost instrumentation and corpus evaluation remain open.
