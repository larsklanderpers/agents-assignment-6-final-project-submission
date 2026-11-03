# Dependent lookup optimization — pending approval

The first human-approved seven-test operation is VERIFIED. Its resulting tree,
`3470718602111dffa871d71cd8ae7d6f1665e2cb`, was reconstructed as an immutable new
baseline without altering the prior operation workspace. The new candidate binds
that exact tree and the prerequisite operation ID.

Four fresh ADK reviews examined the same production source plus the accepted
tests. The ADK synthesis agent revised the plan to version 2: the verified
characterization prerequisite now makes the lookup refactor ready. The input-type
conflict was resolved by a restricted fast path plus an unchanged fallback.
SQL repair and public API naming conflicts remain unresolved and outside scope.
The ADK patch author then proposed the new source file. This preparation used
six bounded model calls (four reviewers, synthesis, patch author).

## Exact proposed change

Six lines are added inside Common_Items. Set lookup is used only when both inputs
are exact built-in lists or tuples and every element is an exact int, bool, str,
bytes or NoneType. The result still iterates the left input, preserving its order
and duplicates. Other input types use the original loop: nested unhashable values,
generators, custom objects and subclasses retain their existing handling. Function
and parameter names, SQL code and the accepted test file are unchanged.

This consumes extra memory for a lookup set. Average-case speed improvement is
expected for ordinary built-in data; no speedup is claimed for fallback inputs
or pathological hash collisions. There is no measured candidate result yet.

- [Exact patch](artifacts/optimization/candidate/candidate.patch)
- [Manifest](artifacts/optimization/candidate/manifest.json)
- [Version 2 plan](artifacts/optimization/plan.json)
- [Fresh reviews](artifacts/optimization/reviews.json)

Patch SHA-256:

    8ffe7d0ab64abe394ebe941c0d4cedd89225d21844ebc042a696b2df10bbd77b

Open `approve-optimization.cmd` and read the diff. To authorize this exact source
patch and its bound checks, enter:

    approve 8ffe7d0ab64a

Other decisions are reject, redirect, defer or cancel. The first approval is
already consumed and cannot authorize this change. This approval is single-use
with 30-minute validity from issuance, not from when the screen was opened.

## Verification before approval

Source syntax, preservation of SQL/function signature, exact single-file diff,
Git applicability, fresh review provenance, verified prerequisite, revised plan
readiness and policy bindings passed. Twenty planning/approval regression tests
and two independent simulated source-patch tests passed. The new runner passed
the seven unchanged tests and 13 extra reference-behavior checks against the
already approved baseline only. No optimization candidate code was executed.

## Checks authorized by the new decision

Apply only collection_ops.py in a new disposable detached workspace. Keep the
accepted test file byte-identical. Run the seven tests and 13 additional
reference checks in the pinned offline non-root Docker container. Extra checks
include mixed/unhashable values, tuples, generators, custom equality/hashing,
subclasses and input preservation. Reference checks compare against the accepted
parent implementation, not against a model-provided oracle.

Then benchmark equivalent results on 2,500 built-in integers: five warmups and
20 trials per version, reporting medians and ranges. Candidate median must be
lower for this bounded case. These are elapsed-time measurements, not operation
counts; the plan now says benchmarks. No fabricated complexity measurements are
reported. Wall-time noise and case specificity remain limitations.

The runner policy binds the harness and bootstrap digests. No host mounts,
credentials or Git metadata enter the container. Failed verification quarantines
the workspace. It does not automatically edit code or skip a fresh approval.
After real execution, inspect artifacts/optimization/candidate/ledger.sqlite,
the LangGraph checkpoint and per-operation logs for actual results.
