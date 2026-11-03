# Corrected characterization expectation — 2 November 2026

The second fresh human-approved attempt completed its Docker run and correctly
reported **FAILED**, rather than an infrastructure error. The model-authored
`test_preserves_left_duplicates` asserted the wrong order:

```python
left = [1, 2, 1, 3, 1]
right = [1, 3]
# Wrong generated expectation: [1, 1, 1, 3]
self.assertEqual(Common_Items(left, right), [1, 1, 3, 1])
```

The reviewed production function preserves left-input order. The correction
changes only this expected literal in the proposed test file. Production source,
the other six tests, reviewed parent, and plan remain unchanged. This is a
developer-corrected proposal, not a fresh model-generated replan.

## Preserved attempts

| Candidate | Operation | Actual outcome |
|---|---|---|
| `candidate-93a15f976a12-exec-v1` | `728750cb5b444beda6a05698bbe0e1ee` | AMBIGUOUS after apply: Windows path enumeration failure; quarantine retained |
| `candidate-93a15f976a12-exec-d24e41f5` | `7e83013f61a549dd98bb5ebee2ffc7e6` | FAILED: seven tests, one wrong-expectation failure; quarantine retained |

Both consumed human approvals remain bound to their original candidates. Before
and after correction, **all 79 files** in the two attempt directories and their
external quarantined workspace were hashed and matched exactly. The comparison
manifests are retained at the run root as `preserved-attempts-before-correction.json`
and `preserved-attempts-after-correction.json`. No ledger, checkpoint, failed log,
patch, quarantine or grant was rewritten or reused.

## Static check and verified tests

`proposal_checks.py` parses AST and uses `ast.literal_eval` on bounded builtin
literal data. It checks concrete, straight-line `assertEqual(Common_Items(...),
expected)` examples against the declared order-preserving membership contract.
It does not import or execute the candidate tests or production code. Dynamic
expectations are rejected; unsupported calls invalidate tracked literal inputs.
It rejects the original `[1, 1, 1, 3]` expectation and accepts `[1, 1, 3, 1]`.

The guard runs during fresh test authorship and executor gate preparation, so
`replace-tests` cannot prepare the unchanged wrong proposal again. Rejected new
author output is retained with static validation diagnostics. This is a bounded
literal-example check, not a proof of full test semantics, safety or coverage.
It checked six literal examples in this proposal; the mutation check is verified
by actual execution instead.

`amend_tests.py` verified the **exact corrected bytes** before creating the new
human gate. It used a separate cloned baseline, an explicitly simulated approval
and ledger, and the same pinned offline Docker executor. No real approval was
entered, copied or consumed by verification. Actual result: **7 tests passed,
0 failures, 0 errors, 0 skips**; the baseline remained `no_tests`.

Retained verification:
`artifacts/runs/packaging-rehearsal-20261102/artifacts/check-32a6e3d26914/verification.json`.
Candidate log SHA256:
`99ee400a9cf33a72aeea03921959531301a7c41c9363cc844dfbd8d245ab424c`.
The corresponding simulated ledger and baseline/candidate logs remain beside it.
These results prove the corrected tests passed in simulation; they do not label
the new human-gated operation VERIFIED.

The complete updated regression suite also passed: **39 tests in 48.219 seconds**,
including a regression proving the wrong expectation blocks gate preparation
before Docker preflight.

## Human gate at preparation (subsequently VERIFIED)

Candidate: `candidate-32a6e3d26914-exec-v1`.
Patch SHA256:
`177fba7497b1b2d26c2f800790685240e9acfea46df7c7d832672e12bd815b01`.
`run.json` selects this candidate and retains both earlier pointers. Its manifest
identifies developer correction, the failed operation/log and the independent
verification report hash. It starts with no real decisions or operations.

```powershell
.venv\Scripts\python.exe review_ledger.py review-tests --run packaging-rehearsal-20261102
```

Personally inspect the displayed candidate and diff before deciding. Its current
decision text is `approve 177fba7497b1`. The real endpoint will execute the tests
again after approval, under the new candidate binding. A preflight simulation
does not authorize an edit or transfer an old approval.

## Subsequent real human-approved outcome

Lars approved this corrected candidate in the interactive endpoint. Operation
`a27c01f604c34003a1bb1124713b81d3` reached VERIFIED: seven tests passed, zero
failures/errors/skips, accepted tree `354b8b75e4037b37167e4cbf531d0b24b2500e1e`.
The real decision and log hashes were checked separately from the simulation.
The command above now displays a completed saved result; do not call reopening
it a fresh approval or test execution. See FRESH-REHEARSAL-RESULT.md for the next gate.
