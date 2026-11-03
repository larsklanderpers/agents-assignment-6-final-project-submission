# Repair verified — failure/replanning scenario completed, 2 November 2026

The separately approved repair operation `25d22a7e90b144a3a562fbf63a0fd608`
reached VERIFIED. Seven original tests and thirteen reference-behavior checks
passed, with no failures, errors or skips. Process exit was 0.

On the bounded 2,500-integer timing case (five warmups, twenty trials/version),
median time was 94.421 ms for the original and 0.527 ms for the repair, about
179x on this case only. Trial ranges were 42.385–152.023 ms and 0.489–0.890 ms.
This is neither a general workload claim nor an operation-count measurement.

Independent inspection verified manifest/approval binding, both log digests,
resulting tree, unchanged accepted tests and completed VERIFIED checkpoint.
The original failed workspace remains quarantined and the parent baseline is
clean. The earlier successful optimization remains untouched.

## Demonstrated sequence

1. A human approved a disclosed negative-case source patch.
2. Actual tests found its nested-list TypeError; the operation FAILED.
3. The failed workspace was quarantined; no failed code entered the accepted chain.
4. The real ADK planner used those logs to revise plan 3 to plan 4 and change
   the dependency graph. The patch author proposed a guarded correction from
   the last verified parent.
5. Replay of the old approval against the new candidate was rejected.
6. The human separately approved the new exact diff.
7. The repair passed all bound checks in Docker and reached VERIFIED.

Coordinator readiness was then recomputed from the actual verified ledger result.
The dependent follow-up is now eligible for proposal; it has not been approved
or executed. The snapshot of trusted completion/readiness is stored in
`artifacts/failure-demo/completion.json`.

Patch: `1722714a87aa12e94e94ec9ed9c271202233bc8720a6d3a7db206e79affaf938`

Accepted repair tree: `d58ca79475a8fae1511101fafe00cbed83dd7286`

Evidence: `artifacts/failure-demo/repair/`, with logs under
`operations/25d22a7e90b144a3a562fbf63a0fd608/`. Inspection did not rerun tests.
Nothing was pushed or merged. This completes the bounded failure-and-replanning
demonstration, not the capstone as a whole. Corpus evaluation, reproducible
fresh-clone packaging and submission documents/recording remain outstanding.
