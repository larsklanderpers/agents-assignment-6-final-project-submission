# Additional Python intake and evaluation

This branch extends the assessed prototype. It does not replace the preserved
rehearsal path or claim that all three material gaps have been resolved.
All new experiment artifacts live under `artifacts/hardening/` and are excluded
from source exports. No old live ledger, grant, workspace or checkpoint is reused.

## Committed Python intake

```powershell
.venv\Scripts\python.exe repository_intake.py --repo ..\agents-assignment-5 --path backend/guardrails/output_filter.py --path backend/guardrails/input_validator.py --path tests/test_guardrails.py --output artifacts/hardening/assignment5-intake-v1.json
```

Use a new output filename each time. Defaults to committed HEAD; use `--revision`
for a specific commit and optional `--base` for a pinned local revision comparison.
Working-tree edits are excluded and reported. Selection is limited to 40 files,
128 KiB per file and 512 KiB total. Symlinks, submodules, path escapes, binary
content and common credential patterns are rejected. This is not a complete
secret scanner: inspect selected source before sending it to a model.

The snapshot records commit/tree, per-file Git object and SHA256, file roles,
coverage limits and a canonical snapshot digest. No repository code, package
installation, hooks, imports or tests are run by intake. GitHub PR retrieval and
general live repository patch execution are not implemented by this milestone.

## Repository review and precision experiment

```powershell
.venv\Scripts\python.exe hardening_review.py --snapshot artifacts/hardening/assignment5-intake-v1.json --contracts evaluation/assignment5-contracts.json --output artifacts/hardening/my-review
```

Four ADK specialists receive the selected files, visible tests, explicit behavior
contracts and numbered source lines. Findings carry path, line, literal evidence,
category, contract ID, consequence, and defect/hypothesis/suggestion disposition.
Only unique contract-referenced defects pass the structural filter. Other findings
remain visible in evidence. The filter does not prove semantic truth; it must be
evaluated for both false positives and missed defects. An invalid citation rejects
the review before planning. Raw responses and usage are retained, including errors.

Assignment 5 source transmission to the configured Gemini service was explicitly
authorized by Lars for these experiments. Credentials and environment files are
not part of model context. No new approval is implied for live code changes.

## End-to-end development pilot

```powershell
.venv\Scripts\python.exe -m evaluation.build_assignment5 --snapshot artifacts/hardening/assignment5-intake-v1.json --output artifacts/hardening/my-corpus.json
.venv\Scripts\python.exe -m evaluation.end_to_end --manifest artifacts/hardening/my-corpus.json --output artifacts/hardening/my-oracle-check --preflight-only
.venv\Scripts\python.exe -m evaluation.end_to_end --manifest artifacts/hardening/my-corpus.json --output artifacts/hardening/my-evaluation --max-attempts 2
```

The corpus builder derives three development cases from Assignment 5's output
filter at commit `3ec39333b23cbcb67bbdd87bcec68fb2914029af`: the original as a
control, a deliberately omitted email mask, and a deliberately weakened account
mask. The original repository is never edited. Source comments preserve the
assignment's distinction between given patterns and student implementation.

The existing assignment check_ harness is retained as review context; it is not
misrepresented as unittest-discoverable. Newly authored visible and hidden stdlib
tests exercise the documented masking contracts. The manifest/hash are frozen
before evaluation. Hidden tests, labels, seeded-mutation description and reference
source are excluded from model inputs. Failure feedback contains real outcome
counts, not hidden assertion text. All model prompts/raw outputs are inspectable.

Each assigned case runs baseline checks, four-agent review, generated plan and
source proposal, a persistent LangGraph gate, an explicitly simulated exact-bound
ledger decision, and independent Docker acceptance. A failed proposal is retained;
a second generated plan/proposal can use its failure counts, with a new grant.
Each retry starts from the original parent. No files are adopted into Assignment 5.

The pilot permits one source step per plan and at most two attempts. Public
function signatures and imports are protected; tests are not editable. Docker
uses the existing pinned offline image, no host mounts/credentials, resource
limits and bounded logs. Structural restrictions do not prove arbitrary Python
is safe; execution remains inside the container.

Report complete-case success over every assigned case, including failed reviews,
abstentions and exhausted attempts. Clean cases must avoid patches to count as
successful. Review scores use provisional category/function matching and count
failed reviews as missed labelled findings. Simulated grants test machinery, not
human judgment. This new evaluator is experimental and is not the legacy live
approval entry point.

## What remains before broader claims

- Assignment 5 is already inspected: all current cases are development cases.
- Three cases do not establish 0.80 precision/recall or general repository repair.
- Run controlled baseline-versus-hardened comparisons on identical snapshots,
  with multiple repeats, human-adjudicated labels and a newly frozen holdout.
- Add multi-file repairs, richer dependent plans and forced recovery cases before
  claiming those dimensions have corpus coverage.
- Verify live repository-specific acceptance/approval contracts separately before
  exposing real mutation commands. PR fetch and stale-head checks remain additional.

The primary recording follows the rubric-focused checkpoint. If this expansion
is completed and independently verified in time, a second recording may show it,
subject to instructor submission rules. Neither recording should imply unmeasured
results or erase the original missed targets.
