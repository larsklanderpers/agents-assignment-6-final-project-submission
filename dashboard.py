"""Local, read-only evidence viewer. No executor imports or mutation endpoints."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sqlite3
from contextlib import closing
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit, parse_qs

ROOT = Path(__file__).resolve().parent


def read_json(path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding='utf-8'))


def run_home(root, identity):
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]{0,79}', identity):
        raise ValueError('Invalid run ID')
    base = (root / 'artifacts/runs').resolve()
    home = (base / identity).resolve()
    if home.parent != base or not (home / 'run.json').is_file():
        raise ValueError('Run not found')
    return home


def snapshot(root, identity):
    home = run_home(root, identity)
    warnings, candidates = [], []
    for path in sorted(home.glob('artifacts/**/manifest.json')):
        if home not in path.resolve().parents:
            continue
        try:
            manifest = read_json(path)
            if 'candidate_id' not in manifest:
                continue
            directory = path.parent
            patch_path = directory / 'candidate.patch'
            if home not in patch_path.resolve().parents:
                raise ValueError('Evidence outside run')
            patch = patch_path.read_bytes()
            operations, decisions = [], []
            db = directory / 'ledger.sqlite'
            if db.exists():
                if home not in db.resolve().parents:
                    raise ValueError('Ledger outside run')
                with closing(sqlite3.connect(db.resolve().as_uri() + '?mode=ro', uri=True, timeout=1)) as connection:
                    connection.row_factory = sqlite3.Row
                    operations = [dict(row) for row in connection.execute('SELECT * FROM operations')]
                    decisions = [dict(row) for row in connection.execute('SELECT * FROM decisions')]
                for op in operations:
                    op['result'] = json.loads(op['result']) if op.get('result') else None
                    op['mode'] = next((d['mode'] for d in decisions if d['id'] == op['approval']), 'unknown')
                    if re.fullmatch(r'[0-9a-f]{32}', str(op['id'])):
                        op_home = directory / 'operations' / op['id']
                        log = op_home / 'candidate.log'
                        if log.is_file() and home in log.resolve().parents:
                            raw = log.read_bytes()
                            op['log'] = raw[:65536].decode('utf-8', errors='replace')
                            expected = (op['result'] or {}).get('candidate', {}).get('log_sha256')
                            op['log_matches'] = hashlib.sha256(raw).hexdigest() == expected if expected else None
                        workspace = root / 'artifacts/ws' / op['id'] if (op_home / 'workspace-location.json').exists() else op_home
                        op['quarantine_present'] = (workspace / 'quarantined_workspace').is_dir()
            relative = directory.relative_to(home).as_posix()
            simulated = any(d.get('mode') == 'simulated' for d in decisions) or bool(re.search(r'preflight|simulat', relative, re.I))
            candidates.append({'path': relative, 'manifest': manifest, 'patch': patch.decode('utf-8'),
                               'patch_matches': hashlib.sha256(patch).hexdigest() == manifest['patch_sha256'],
                               'operations': operations, 'decisions': decisions, 'simulated': simulated})
        except (OSError, ValueError, KeyError, sqlite3.Error) as error:
            warnings.append(f'{path.parent.relative_to(home)}: evidence unavailable ({type(error).__name__}); refresh to retry.')
    def optional(name):
        path = home / name
        try:
            if home not in path.resolve().parents:
                raise ValueError('Evidence outside run')
            return read_json(path, {})
        except (OSError, ValueError):
            warnings.append(f'{name}: unavailable or being updated.')
            return {}
    return {'run': identity, 'record': optional('run.json'),
            'reviews': optional('artifacts/live-spike/result.json'),
            'initial_plan': optional('artifacts/plan-spike/result.json'),
            'current_plan': optional('artifacts/failure-demo/current-plan.json'),
            'replanning': optional('artifacts/failure-demo/replanning-evidence.json'),
            'session': optional('rehearsal-session.json'), 'candidates': candidates, 'warnings': warnings,
            'comparison': read_json(root / 'results/comparison.json', {})}


def handler(root):
    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            # Reject foreign Host headers (including DNS rebinding); never enable CORS.
            if self.headers.get('Host') not in {f'127.0.0.1:{self.server.server_port}', f'localhost:{self.server.server_port}'}:
                self.send_error(403)
                return
            url = urlsplit(self.path)
            try:
                if url.path == '/':
                    body = (root / 'dashboard.html').read_bytes()
                    mime = 'text/html; charset=utf-8'
                elif url.path == '/api/runs':
                    base = root / 'artifacts/runs'
                    runs = sorted([p.parent.name for p in base.glob('*/run.json') if p.parent.resolve().parent == base.resolve()], reverse=True)
                    body = json.dumps(runs).encode()
                    mime = 'application/json'
                elif url.path == '/api/run':
                    body = json.dumps(snapshot(root, parse_qs(url.query).get('id', [''])[0])).encode()
                    mime = 'application/json'
                elif url.path == '/api/comparison':
                    body = json.dumps({'text': (root / 'results/COMPARISON.md').read_text(encoding='utf-8')}).encode()
                    mime = 'application/json'
                else:
                    self.send_error(404)
                    return
            except (OSError, ValueError, KeyError, sqlite3.Error):
                self.send_error(503, 'Evidence unavailable; refresh to retry')
                return
            self.send_response(200)
            self.send_header('Content-Type', mime)
            self.send_header('Cache-Control', 'no-store')
            self.send_header('X-Content-Type-Options', 'nosniff')
            self.send_header('Content-Security-Policy', "default-src 'self'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; connect-src 'self'; frame-ancestors 'none'; base-uri 'none'")
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass
    return Handler


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--port', type=int, default=8765)
    args = parser.parse_args()
    server = ThreadingHTTPServer(('127.0.0.1', args.port), handler(ROOT))
    print(f'Review Ledger: http://127.0.0.1:{server.server_port} (read-only; Ctrl+C to stop)', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
