# Dependent optimization — VERIFIED, 1 November 2026

One real interactive approval was consumed by operation
`078e14ef548e49978f293f66a82d30a7`. The resulting state is VERIFIED.

- Seven existing tests passed, with zero failures, errors or skips.
- Thirteen additional reference-behavior checks passed, including generators,
  custom equality, subclasses, unhashable values and input preservation.
- The before/after timing check passed on 2,500 built-in integers, with equivalent
  output, five warmups and twenty trials per version inside the same container.

| Measurement | Original | Candidate |
|---|---:|---:|
| Median | 115.379 ms | 0.620 ms |
| Observed trial range | 108.914–172.790 ms | 0.570–0.893 ms |

The measured median ratio was approximately 186x on this single synthetic
fast-path case. This is not a general workload speedup or a measured complexity
bound. Fallback inputs retain the original loop; the fast path uses extra memory.

Independent inspection confirmed approval/manifest binding, both log digests,
accepted source tree, unchanged test bytes and completed LangGraph checkpoint.
The parent baseline is clean. No checks were rerun during inspection. Only the
disposable workspace contains the applied optimization; nothing was pushed or
merged into the project checkout.

Patch: `8ffe7d0ab64abe394ebe941c0d4cedd89225d21844ebc042a696b2df10bbd77b`

Resulting tree: `54b613b65bf2d39ee3b88e25d53ff4ae023afaaf`

Evidence is in `artifacts/optimization/candidate/`, with logs under
`operations/078e14ef548e49978f293f66a82d30a7/`. The approval ledger records one
interactive decision and one operation. This demonstrates the successful
test-prerequisite → revised plan → separately approved refactor chain.

Remaining capstone work includes a live failure/replanning demonstration,
reproducible corpus evaluation, fresh-clone packaging, updated reflection and
the combined presentation/demo recording. These results do not imply completion
of the complete assignment or absence of other findings, such as the SQL issue.
