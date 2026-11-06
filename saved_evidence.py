"""Read-only display of preserved, previously human-approved operations (SAVED)."""
import hashlib
import json
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
CASES = [('tests', 'first-patch/candidate-c2a7ed975417-exec-v1'),
         ('optimization', 'optimization/candidate'),
         ('controlled_failure', 'failure-demo/fault'), ('repair', 'failure-demo/repair')]


def inspect():
    output = {'mode': 'SAVED HISTORICAL EVIDENCE; no new execution', 'operations': []}
    for label, relative in CASES:
        directory = ROOT / 'artifacts' / relative
        ledger = directory / 'ledger.sqlite'
        if not ledger.exists():
            output['operations'].append({'label': label, 'available': False,
                'reason': 'Local ignored evidence is absent; see published result documents.'})
            continue
        manifest = json.loads((directory / 'manifest.json').read_text())
        binding = hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest()
        with sqlite3.connect(ledger.as_uri() + '?mode=ro', uri=True) as db:
            db.row_factory = sqlite3.Row
            for operation in db.execute('SELECT * FROM operations'):
                row = dict(operation)
                result = json.loads(row['result'])
                operation_dir = directory / 'operations' / row['id']
                logs = {phase: hashlib.sha256((operation_dir / (phase + '.log')).read_bytes()).hexdigest() == result[phase]['log_sha256']
                        for phase in ('baseline', 'candidate')}
                output['operations'].append({'label': label, 'available': True, 'id': row['id'],
                    'state': row['state'], 'post_tree': row['post_tree'],
                    'binding_matches': row['binding'] == binding, 'log_hashes_match': logs,
                    'result': result, 'quarantined': (operation_dir / 'quarantined_workspace').exists()})
    return output


if __name__ == '__main__':
    print(json.dumps(inspect(), indent=2))
