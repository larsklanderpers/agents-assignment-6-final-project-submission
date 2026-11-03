# Failure and replanning demonstration

This is a disclosed controlled negative-case branch, not a failure of the already
successful optimization. That successful operation and its workspace are retained.
The demo starts again from the accepted seven-test parent snapshot. Complete
four-specialist reviews are reused because that source and test snapshot is
byte-identical. No external service is deliberately disrupted.

## First human decision: deliberate failure

Open `approve-failure-demo.cmd`. The exact diff proposes an unguarded set lookup,
known to fail for nested lists. This is proposal-layer fault injection before
approval; no approved patch is modified afterward. It is not an AI-generated
claim of a safe optimization. The user request supplies direction for a controlled
negative case; it does not substitute for exact-patch approval.

After reviewing the diff, enter:

    approve 99d40a18b4f6

The system should apply that exact patch only in a new disposable workspace, run
the unchanged seven tests in Docker, record the real TypeError, mark the operation
FAILED and quarantine its workspace. The original baseline and successful
optimization remain unchanged. The negative case must never enter an accepted
patch chain. Its dependent follow-up remains blocked.

An expected failure is a successful demonstration of rejection, not a passing
refactoring operation. If an unrelated setup failure occurs, disclose that and
resolve it rather than claiming the intended test failure occurred.

## Replanning and second human decision

Tell Codex when the first run finishes. It will inspect the actual ledger and
test logs. Replanning is allowed only after a real FAILED operation with the
expected unhashable-value evidence and a quarantined workspace exists.

The real ADK synthesis/planner receives that evidence, revises demo plan version
3 to 4, records the failed assumption and directs a guarded repair against the
last verified parent. The patch author proposes a new exact diff. The failed
step remains historical/deferred; the descendant depends on the new repair and
cannot run before its verification.

The new plan invalidates version-3 execution bindings. A direct old-approval
replay check must reject the old grant without creating another operation. No
descendant approval is fabricated; this scenario demonstrates rejection of
reuse of the consumed old grant, plus plan-version invalidation. No claim is
made that an actually approved descendant existed.

Open `approve-demo-repair.cmd` only when the new proposal is ready. Read its diff
and use the NEW approval text displayed there. Approval of the failure case does
not approve the repair. The corrected candidate must pass seven original tests,
thirteen reference checks and the same bounded timing check before VERIFIED.

## Current preparation evidence

Three demo-policy tests passed: direction is required for the intentional negative
case, descendants cannot bypass prerequisites, missing verified context blocks
preparation, and the injected proposal preserves SQL and the public signature.
The fault runner was checked on the already-approved good baseline only. No real
fault candidate is executed before human approval.

Artifacts are under `artifacts/failure-demo/`: versioned plans, direction record,
candidate diffs, checkpoint/decision/operation ledgers and logs. Runtime state
must be inspected after each actual decision. Replanning uses two bounded live
model calls (planner and patch author), clearly separate from cached reviews.
There is no automatic code repair, push, merge or deployment.
