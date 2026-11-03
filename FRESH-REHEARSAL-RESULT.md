# Fresh rehearsal results - checked 3 November 2026

The bounded human-approved test/optimization/failure/replanning/repair chain is
now verified in run `packaging-rehearsal-20261102`. This is separate from the
original four historical operations. It is saved execution evidence, not a
measured spoken rehearsal or completed recording.

| Stage | Real operation | Saved outcome |
|---|---|---|
| Corrected characterization | `a27c01f604c34003a1bb1124713b81d3` | VERIFIED: seven tests |
| Optimization | `14ba9fa431624649bfd5771169957cb3` | VERIFIED: seven tests + thirteen checks |
| Disclosed negative case | `22f6b9be80134420b4d64c92af8659d0` | FAILED: seven tests, one nested-list TypeError; quarantine retained |
| Separately approved repair | `bde81e424c184be6b33ecd79b92fec35` | VERIFIED: seven tests + thirteen checks |

All four decisions were interactive, consumed by their own operations. The repair
patch SHA256 is `a0540b3e4776a612784fbfb2c424b6992660a911a2f528cfdee27694c8df47ef`;
its accepted tree is `328a73f2634c3c68619ea79d3773c28e1e606a06`. The actual repair
candidate log SHA256 is
`c0a168c83c327628cd17a57c733f785a551bea047cac7a2d44d3d77bdc33250b`.

## Saved-evidence audit

Read-only checks confirmed, for each stage: exact manifest/approval/operation
binding, consumed interactive decision, patch digest, both log hashes, terminal
checkpoint candidate/approval/outcome, and actual source/test bytes matching every
file in the recorded result tree. Git object reads were used rather than
reapplying patches or staging files. Core manifests, patches, ledgers and
checkpoints had identical hashes before and after the audit.

Audit record:
`artifacts/runs/packaging-rehearsal-20261102/artifacts/failure-demo/completion.json`.
The failed workspace remains quarantined. All 79 evidence files from the earlier
AMBIGUOUS Windows-path attempt and FAILED wrong-expectation attempt also remain
unchanged. Original historical runs have not been restarted.

The real repair's 2,500-integer benchmark used five warmups and twenty trials:
median **97.368 ms before / 0.539 ms after**. Observed ranges were 40.504-161.831 ms
and 0.502-0.870 ms. This is elapsed time for one synthetic case, with extra memory;
it is not a general speedup claim. Simulated preflight timings remain separate.

## Planning and remaining authority

Actual failure logs drove live plan revision 3 to 4. The failed action was deferred,
the repair used the last VERIFIED test-bearing parent, and the follow-up was
redirected to the repair. Old approval replay was rejected without another
operation. Now that the real repair is VERIFIED, the follow-up is eligible for a
proposal, but it remains **unauthorized and unexecuted**. It is not needed for the
demo. No additional patch approval is pending in this completed chain.

## Preparation history and limits

The first generated characterization tests had a wrong expected ordering; the
corrected expectation, static guard, separate simulated preflight and subsequent
real approval are documented in TEST-EXPECTATION-CORRECTION.md. Optimization
preparation exposed a trusted-harness path assumption; the live source/reviews
were retained, but the missing original rationale was explicitly replaced by a
labeled developer summary rather than reconstructed as a model quote.

The first repair-plan response was rejected by readiness/dependency validation;
its raw output had not been saved, and that limitation is recorded. The next
validated plan and raw author output were retained. Two whitespace-filled blank
lines were normalized outside string literals before proposing the exact repair;
AST equivalence was checked. See REPAIR-REVIEW-2026-11-03.md and the retained
replan-attempts directory. The latest implementation regression suite passed
42 tests in 50.089 seconds; the evidence audit did not rerun approved operations.

## Thursday readiness

Reopening a completed test/optimization/repair command displays its recorded
outcome. The version-3 fault gate is invalid after plan revision. Use a new run ID
for a fresh live segment; keep this completed run as labeled saved fallback.
The full spoken <=10-minute rehearsal, recording, document page counts,
implementation publication/instructor access and Canvas checks remain outstanding.
See THURSDAY-DEMO-CHECKLIST.md and DEMO-RUNBOOK.md.
