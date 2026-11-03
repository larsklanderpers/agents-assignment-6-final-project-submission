# First candidate patch — ready for review

Prepared 1 November 2026 by the real ADK patch-author agent using Gemini 3.8
Flash, following the saved plan's eligible collection-characterization action.
The four reviews and synthesis are reused evidence, not rerun during authoring.

One new file is proposed: `tests/test_collection_ops.py` (43 lines, seven tests).
Production code is unchanged. The tests characterize:

1. Empty left input returns an empty result.
2. Empty right input returns an empty result.
3. Results preserve the left input's order.
4. Matching duplicate values in the left input remain duplicated.
5. Duplicate values in the right input do not multiply the result.
6. Nested lists work even though they cannot be put in a set.
7. Neither input list is modified.

The nested-list check matters: a naive set-based optimization could fail it.
These are concrete behavioral assertions, not tests reproducing the loop logic.
The SQL function is outside this step. Generators, arbitrary custom equality and
non-iterable inputs are not covered; this is a bounded characterization suite.

## Inspect the exact proposal

Candidate: `candidate-c2a7ed975417`

- [Candidate diff](artifacts/first-patch/candidate-c2a7ed975417/candidate.patch)
- [Bound metadata and checks](artifacts/first-patch/candidate-c2a7ed975417/manifest.json)
- [Original synthetic source](artifacts/first-patch/baseline/collection_ops.py)

These links refer to local ignored artifacts, not uploaded repository files.

Patch SHA-256:

    ad012a47b76d864c49cec2f20e57ed66fe9ccdcdd82f82ff84dbfa06e4a332c2

Parent commit: `9828f0900118f74a7937f39b67ec3c6f5df64173`

Parent tree: `0934c950d11e41ed8ec0232445838d41260aa4d1`

Plan version: 1; step: `act-char-common-items`. Candidate metadata also binds the
plan digest, review artifact digest, scope and initial runner policy digest.

## Verification and approval boundary

Python syntax parsing passed without executing the proposed tests. Git's
`apply --check --whitespace=error` passed against the clean pinned baseline;
that command did not apply the patch. Inspection found only unittest assertions
and imports of unittest and the target function. No model-provided shell command
is accepted. LangGraph persisted the candidate at an interrupt.

The target test file does not exist in the baseline. Test execution is **not run**;
there is no pass claim. No approval has been issued, so no approval expiry clock
is running. The candidate can remain deferred while the human reviews it.

The Python 3.12.14 container image has been downloaded and its startup verified
with no network, read-only filesystem, non-root user, dropped capabilities and
resource limits. Image digest:

    sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f

The startup check printed only Python's version; it did not mount or run target
code. This is not yet an implemented test executor. Before collecting executable
approval, finalize and bind that image and export/isolation settings in the runner
policy, implement the interactive operator decision and atomic operation ledger,
and revalidate all bindings. Approval of this coverage discussion alone must not
be treated as authorization to apply the patch. Test edits follow the same
exact-patch approval rule as production changes.

## Git preservation

Authenticated cloning succeeded. Original history was copied into the existing
project only after checking that it had no Git metadata. The original staging
clone is retained at `../capstone-git-staging`. Branch `implementation/first-patch`
is based on design commit `4c4ca01`; local source, documentation, environment and
evidence were preserved. Existing secret-ignore patterns were retained and
`artifacts/` added. Nothing has been pushed.
