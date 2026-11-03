# Bounded repository repair workflow

Run from the project directory using `.venv\Scripts\python.exe`. These commands
are additional to the original rehearsal. They never grant approval on your behalf.
Use a NEW output directory for each preparation, retry and evaluation.

## Local intake and first candidate

Provide a clean committed repository, explicit behavior contracts in a JSON
object, and Python source plus discoverable `tests/test_*.py` unittest tests.
No dependencies are installed. Configuration files are context, not execution
instructions. Selecting a subset does not claim whole-repository coverage.

```powershell
.venv\Scripts\python.exe prepare_repository_repair.py --repo PATH --contracts contracts.json --output artifacts/hardening/NEW-RUN
```

Optional repeatable `--path` selects files; `--revision` defaults to HEAD.
The workflow measures baseline tests, invokes five reviewers, plans and authors
a bounded candidate. It stops if the baseline fails or no supported issue exists.
Missing dependencies are diagnostic failures, not permission to install packages.

## Personal terminal approval

For the already prepared, deliberately seeded Assignment 5 development example:

```powershell
.venv\Scripts\python.exe repository_repair.py review artifacts/hardening/assignment5-local-repair-20261104-v1/preparation/candidate
```

Read the exact diff, origin, plan, tests and limits. Personally type the exact
displayed `approve <hash>` or reject/redirect/defer/cancel. Do not pipe decisions.
Each approval is bound to the exact candidate, actor and mode, single use, and
expires after thirty minutes. Source and PR freshness are checked again after
the decision wait and before execution. Failed or ambiguous operations retain
their evidence; original source repositories are unchanged.

For a VERIFIED step with more plan steps, or a FAILED step needing a fresh retry:

```powershell
.venv\Scripts\python.exe continue_repository_repair.py --previous-candidate PATH-TO-CANDIDATE --output artifacts/hardening/NEW-CONTINUATION
```

Continuation uses the approved proposal and ledger outcome, not an editable
export as authority. It prepares a new personal approval gate. Ambiguous runs
require inspection, not automatic replay. Final verified exports are not
automatically committed, pushed or merged.

## Public GitHub PR intake

```powershell
.venv\Scripts\python.exe pr_intake.py --url https://github.com/OWNER/REPO/pull/NUMBER --output artifacts/hardening/NEW-INTAKE --path package/module.py --path tests/test_module.py
.venv\Scripts\python.exe prepare_repository_repair.py --pr-intake artifacts/hardening/NEW-INTAKE --contracts contracts.json --output artifacts/hardening/NEW-PR-REPAIR
```

Public GitHub only, no authentication setup. Intake records all changed paths
and pins selected committed source. Closed PRs can be inspected, but cannot
receive live repair approval. If head/base/state changes, prepare a new intake
and candidate. No GitHub comments, branches, pushes or merges are performed.

## Development evaluation

```powershell
.venv\Scripts\python.exe -m evaluation.build_repository_corpus --output artifacts/hardening/NEW-CORPUS.json
.venv\Scripts\python.exe -m evaluation.repository_end_to_end --manifest artifacts/hardening/NEW-CORPUS.json --output artifacts/hardening/NEW-EVALUATION --repeats 2
```

These are simulated approvals and author-known synthetic development cases.
Private acceptance assertions never enter model payloads. Original source,
raw model proposals, deliberately injected failures, quarantines and final
checks remain separate. See REPOSITORY-HARDENING-RESULTS.md for measured outcomes
and limits; do not interpret this development score as unseen accuracy.
