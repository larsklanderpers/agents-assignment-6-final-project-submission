# Actual failure and replanning — 2 November 2026

## Observed failure

The operator approved the disclosed negative-case patch. Operation
`8a0b2ee93b004e378682d2ec7805c293` reached FAILED. The good baseline passed
seven tests and thirteen reference checks. The faulty candidate ran seven tests:
six passed and the nested-list test raised `TypeError: unhashable type: 'list'`
at `lookup = set(other)`. Candidate process exit code was 1.

Both log digests, approval binding, quarantined source bytes and completed FAILED
LangGraph outcome were independently checked. The failed workspace is quarantined;
the parent baseline is clean. The previously successful optimization is untouched.
This was intentional proposal-layer fault injection, not an unexpected regression
in the successful operation and not a fabricated tool error.

## Real ADK replanning

The synthesis agent received the actual failure log and operation result. It
revised the demonstration plan from version 3 to version 4:

- Verified characterization remains historical accepted evidence.
- The failed set-only action is deferred, not marked successful.
- A new repair action starts from the last verified parent, not failed code.
- The dependent follow-up now depends on that repair and remains blocked.
- The failed assumption is explicit: original list membership can accept values
  that cannot be inserted into a set.

The patch-author agent then proposed a guarded fast path with the original loop
as fallback. Both model calls are live; the unchanged parent reviews are cached
and explicitly reused. The new code has passed syntax/scope, diff applicability,
provenance, prerequisite and plan checks; it is **not yet applied or executed**.
The model's proposed resolution is not treated as proven until verification.

An actual attempt to consume the old approval against the new candidate was
rejected by the binding check, with no additional operation created. No fictional
approved descendant is claimed: this demonstrates old-grant replay rejection and
plan-version invalidation while the unexecuted follow-up remains blocked.

## New human decision required

Read the new diff in `artifacts/failure-demo/repair/candidate.patch`. The corrected
step still requires a separate approval:

    approve 1722714a87aa

Use `approve-demo-repair.cmd`. Approval will apply only that exact source diff
in a fresh disposable workspace and run seven unchanged tests, thirteen extra
reference checks and the bounded timing benchmark inside Docker. It cannot reuse
permission for the failed candidate. No correction is automatically applied.

Evidence: `artifacts/failure-demo/plan-v3.json`, `plan-v4.json`,
`replanning-evidence.json`, and per-candidate checkpoints, ledgers and logs.
The scenario remains incomplete until the human decides on the repair and its
actual verification result is inspected. No merge, push or deployment occurred.

Subsequent result: the human approved the repair and verification succeeded.
See [RECOVERY-RESULT.md](RECOVERY-RESULT.md) for the completed scenario, actual
test/benchmark results and trusted dependent-readiness update.
