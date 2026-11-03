# Fresh repair review — 3 November 2026

Run: `packaging-rehearsal-20261102`. The repair subsequently reached **VERIFIED** under real human approval.
The preparation notes below are retained as history. See the actual result below.
The successful optimization and all failed/quarantined evidence remain preserved.

## Actual failure and revised plan

The deliberately incorrect set-conversion patch was approved through the real
interactive endpoint and FAILED in operation `22f6b9be80134420b4d64c92af8659d0`:
seven tests, one nested-list `TypeError`, zero assertion failures. Its candidate
log hash is `f847e0b36b1102a8c33180c5193115eaa2394810ddfb0bc1a2599a8228ad1205`.
The failed workspace remains quarantined.

Actual failure logs were passed to the live ADK planner and patch author.
The validated plan moved **3 → 4**:

| Action | Current disposition |
|---|---|
| Characterization tests | Real VERIFIED prerequisite retained |
| Failed set conversion | Deferred as failed history |
| Guarded repair | Proposal based on the last VERIFIED test-bearing parent |
| Dependent follow-up | Depends on the repair; blocked until its real VERIFIED outcome |

The first planner response was rejected by the readiness/dependency check before
any plan revision or repair gate. Its raw output was not persisted by the old
implementation; `replan-attempts/initial-rejection.json` explicitly records that
limitation. It has not been reconstructed or silently counted as a pass.

After clarifying that proposal readiness is not execution authorization, the next
plan passed the same deterministic checks. Raw input, planner output, author
output and validation diagnostics are retained under
`artifacts/failure-demo/replan-attempts/9da3b4341bff/` within this run.

The author output contained two space-filled blank lines, so Git's strict
applicability check rejected its formatting before gate creation. Those raw bytes
are retained. The coordinator removed trailing whitespace only outside string
literal lines; AST comparison confirmed the normalized proposal is equivalent
to the original author output. String contents, SQL, signature and tests were
not changed. Whitespace normalization and its string-preservation tests now
cover future proposals too.

## Repair proposal and independent verification

Candidate: `demo-repair-c136cbeea2`, plan 4.
Patch SHA256:
`a0540b3e4776a612784fbfb2c424b6992660a911a2f528cfdee27694c8df47ef`.
Parent tree: `354b8b75e4037b37167e4cbf531d0b24b2500e1e`.

The patch adds a guarded set fast path for the bounded builtin scalar/container
case and retains the original loop as fallback, including nested-list handling.
It starts from the accepted test-bearing parent, not the quarantined failed tree,
and does not modify the independent VERIFIED optimization branch.

An exact copy passed **seven tests plus thirteen behavior checks** in a separate
explicitly simulated Git/Docker verification. No real approval was issued there.
Five warmups and twenty trials on 2,500 integers gave medians of 95.472 ms before
and 0.529 ms after; that result is specific to this synthetic case and uses extra
memory. The full observed timing range is retained in the report.

Preflight report:
`artifacts/runs/packaging-rehearsal-20261102/artifacts/failure-demo/preflight-repair-ee9d4508/verification.json`.
The real repair ledger has **zero decisions and zero operations**.

The old approval was replayed against the new candidate and rejected, with no
extra operation. `replanning-evidence.json` records that result and the blocked
descendant. The full updated regression suite passed **42 tests in 50.089 seconds**.

## Human review at preparation (now completed)

```powershell
.venv\Scripts\python.exe review_ledger.py review-repair --run packaging-rehearsal-20261102
```

Inspect the exact diff, parent, plan version and acceptance checks before deciding.
The current decision text is `approve a0540b3e4776`.

Approval authorizes this repair only. The real executor must run its own checks
before reporting VERIFIED. The successful simulated preflight does not unblock
the real dependent follow-up or transfer the failed operation's approval.

## Actual approved result and saved audit

Real operation `bde81e424c184be6b33ecd79b92fec35` reached VERIFIED: seven tests
plus thirteen checks passed. The accepted tree is
`328a73f2634c3c68619ea79d3773c28e1e606a06`. The consumed interactive approval,
manifest binding, both log hashes, completed checkpoint and actual workspace files
were checked read-only. The earlier zero-decision statement describes preparation,
not current state. Its approval is consumed; reopening the command shows the
recorded outcome. The follow-up is now eligible for proposal only, not authorized
or executed. See FRESH-REHEARSAL-RESULT.md for the current summary.
