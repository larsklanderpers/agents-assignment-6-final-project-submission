"""An explicitly selected demo owns all of its artifacts; legacy paths stay intact."""
import os
import json
from pathlib import Path

PROJECT = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('REVIEW_LEDGER_RUN_HOME', PROJECT)).resolve()


def first_candidate():
    if ROOT == PROJECT:
        return ROOT / 'artifacts/first-patch/candidate-c2a7ed975417-exec-v1'
    manifest = json.loads((ROOT / 'run.json').read_text())
    if not manifest.get('first_candidate'):
        raise ValueError('First candidate is not prepared; run propose-tests first')
    relative = Path(manifest['first_candidate'])
    result = (ROOT / relative).resolve()
    if not result.is_relative_to(ROOT) or relative.is_absolute():
        raise ValueError('Candidate must belong to selected run')
    return result
