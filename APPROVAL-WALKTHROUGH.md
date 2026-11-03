# First patch approval

Open `approve-first-patch.cmd`. Read the displayed exact diff and acceptance
checks. To authorize the seven-test patch, enter:

    approve ad012a47b76d

Other choices: `reject`, `redirect`, `defer`, `cancel`. Redirection asks for
constraints; rejection, redirection and cancellation require a new candidate.
Deferral leaves the decision pending without starting an approval expiry clock.
No model is called. Approval must come from the interactive local operator;
piped input and simulated approvals are rejected by the normal endpoint.

Approval is bound to the patch, parent, plan, scope, policy and actor, expires
after 30 minutes and is consumed once. A durable lock excludes a second operator
or executor. The SQLite ledger atomically records consumption and operation
intent. LangGraph stores the pending decision and operation reference.

After approval, baseline checks run inside Docker. A zero-test baseline is
reported as `no_tests`, not a passing suite. Only then is the approved test file
applied in a disposable detached Git clone. The original baseline and project
checkout remain unchanged. Only the allowlisted source and test files are
exported to Docker over stdin: no host mounts, Git metadata, keys or Docker socket.
The pinned Python 3.12.14 container has no network, a read-only root, non-root
identity, dropped capabilities, no-new-privileges, bounded temporary storage,
128 MiB memory, 0.5 CPU, 32 processes, 30-second timeout and capped logs.
Verification requires at least seven tests and no failures, errors or skips.

The execution candidate `candidate-c2a7ed975417-exec-v1` preserves the original
diff but binds the finalized runner policy and bootstrap digest. Results go to
`artifacts/first-patch/candidate-c2a7ed975417-exec-v1/`, including the manifest,
checkpoint, approval/operation ledger and logs. Artifacts remain private/ignored.
Failed or ambiguous workspaces are quarantined. Reopening returns a completed
result or reconciles an existing operation; it does not grant a second apply.
Partial/ambiguous cloning stops safely rather than guessing.

Before real approval, 12 approval/recovery tests passed on independent fixtures
with explicitly simulated decisions. Coverage includes expiry, tampering, actor
and mode mismatch, duplicate approvals, lock exclusion, path rejection, missing
isolation, failure quarantine and the crash window after apply. These targeted
tests do not prove exhaustive crash recovery. One real Docker integration check
passed nine internal isolation probes and verified zero-test baseline reporting.
The real pending patch has not been applied or tested by those checks.

This is a bounded first-test slice, not a general arbitrary-repository executor.
Remaining work includes generalized patch handling, automatic replanning,
the dependent optimization and corpus evaluation. Authentication is local
single-user identity, not remote authorization.
