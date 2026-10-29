# Implementation contract

Design decisions tightened on 27 October 2026. These are proposed application contracts, not verified framework APIs. Implement them before adding optional features. They supplement [ARCHITECTURE.md](ARCHITECTURE.md) without expanding its submission narrative.

## Intake and complete review

Accept exactly one mode: local repository + pinned revision; GitHub PR + pinned base/head; or unified diff + pinned base repository. Validate every patch path and base before constructing the intake snapshot. Intake reconstruction reproduces the submitted input; it is not a system-proposed refactoring and grants no change authorization. A context-free diff is read-only and partial. Capture original and materialized tree hashes, selected paths, omissions and provenance.

All four specialists receive the same bounded snapshot, configuration, baseline evidence and scope. They return `complete`, `failed` or `unavailable`, plus reviewed paths and limitations. Empty findings with `complete` differs from no response. Complete status means the assigned bounded review finished, not that the code is safe. Wait for all terminal outputs before synthesis. In the MVP any missing specialist blocks executable changes; a human can retry, end read-only, or select a smaller scope and rerun all four. Human acknowledgment cannot turn a failed review into a completed one.

ADK hosts all six reasoning agents. LangGraph calls the parallel specialist adapter, then the synthesis/planner, then the patch author. The application owns schema validation, stable IDs, reducers, persistence and gate enforcement. Only the coordinator can update authoritative state; agents return proposals. Repository conventions are evidence, not permission to execute arbitrary repository commands.

## Human interface and authorization

Use a local single-user CLI for the MVP. Show category coverage, unresolved conflicts, DAG readiness, exact parent revision, diff, risk, intended behavior delta, acceptance checks and evidence links at each gate. Accept `approve`, `reject`, `redirect`, `defer`, or `cancel`. Redirect captures text constraints and creates a new proposal; it cannot modify an already approved patch in place. Show final per-step and cumulative diffs plus unresolved findings and actual test outcomes.

Approval comes from the interactive operator endpoint, never agent output, repository content or a model tool. Bind the actor to an OS-user-owned local session; record the actor ID. This is a local trust boundary, not production-grade remote identity. A future network UI requires authenticated authorization and is outside the MVP. Evaluation's scripted actor is a separate explicitly enabled mode, tagged `simulated`, disabled in the normal CLI, and excluded from claims of meaningful human review.

Add `issued_at`, `expires_at`, `consumed_by_operation_id` and `status` to Approval. Default validity: 30 minutes from issuance, configurable and recorded in policy. Deferral has no expiry because no approval has been issued; an expired approval requires a fresh decision. Any candidate, parent tree, policy, scope or plan-version change invalidates approval. One active executor per run is enforced by a durable lock and compare-and-set transition. A duplicate resume returns existing operation status rather than granting another execution.

Plan revision invalidates all pending approvals in that run in the MVP. Passed steps remain historical evidence. This conservative rule avoids claiming selective reuse while binding approval to a global plan version. Regenerate every subsequent patch against the latest verified parent, including independent DAG steps: logical independence does not imply an unchanged parent tree.

## Change and replay semantics

The executor alone applies patches, after validating the gate and persisting an operation intent. This covers production code, tests, configuration and recovery edits. Disable auto-fixing tools. Prohibit agent changes to the evaluation harness, hidden labels, authorization code, runtime policy and runner configuration. A patch cannot alter its own acceptance checks after approval. Schema/tool failure is not an invitation to execute free-form shell commands.

Operation states: `PREPARED → APPLIED → VERIFIED` or `FAILED/AMBIGUOUS`. Persist pre/post tree hashes and artifact digests. Bind approval consumption and operation creation atomically in the local ledger; checkpoint references the operation ID. A consumed approval authorizes reconciliation of that operation only, never a different patch. On restart, compare durable intent, recorded tree and actual workspace; resolve known outcomes or reconstruct from the last verified tree. Fresh execution after a failed operation requires a new approval. If checkpoint and ledger disagree, block new writes until reconciled.

Cancellation stops scheduling and terminates bounded runner work; it cannot undo an already applied edit atomically. Quarantine/discard the disposable candidate workspace, retain evidence and return `CANCELLED`. Verified prior patches remain review artifacts. Failed/blocked runs cannot be labeled complete. `COMPLETE` requires four completed reviews, no unresolved blocking conflict, all selected steps verified, and a bundle listing deferred/unfixed findings; it does not mean the repository has no defects.

## Execution boundary and acceptance

Choose a container as the MVP execution boundary, rather than an unspecified ordinary subprocess. No Docker socket mount, host credentials, writable source checkout or host Git metadata is exposed. Drop elevated privileges; disable network; enforce resource/time limits and allowlisted output paths. Worktree isolation alone is insufficient. If the required boundary cannot start, preserve review/proposal functions but block execution. Confirm exact host/container settings in M1/M4; this document does not certify isolation before those checks.

Baseline tests and analysis also execute untrusted repository code and require the same boundary. Never install arbitrary project dependencies on the host. A separate preparation phase resolves pinned dependencies with explicit network policy; test runs use the prepared environment offline. Keep repository tool configuration distinct from trusted runner policy.

Acceptance checks are typed tool specifications selected from an allowlist, not executable strings supplied by the model. Record baseline outcome, candidate outcome and the approved intended behavior delta. Any unavailable required check blocks step verification. Baseline failures may remain only if explicitly identified, unchanged and irrelevant to the approved scope; require relevant tests to pass and label the remaining failures in the bundle. A human cannot override stale approval, path restrictions or required isolation through a comment.

## First vertical slice: implementation acceptance

Before broadening features, demonstrate one tiny repository through real ADK reviews, LangGraph durable wait, human rejection/redirection, exact-patch approval, sandboxed test edit, dependent refactor, injected verification failure and replanning. Produce actual changed code as a diff and cumulative bundle; findings-only output is insufficient. Restart at WAIT_APPROVAL and after APPLY; prove no extra application. The same slice must run from documented fresh setup with locked versions. This is the first implementation target, not work completed by this review.
