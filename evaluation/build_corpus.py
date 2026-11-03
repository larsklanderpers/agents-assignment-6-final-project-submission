"""Original seed-505 corpus. Run once before evaluation; never tune held-out labels."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).parent


def build():
    cases = []
    for split, suffix in [('development', ''), ('held_out', '_variant')]:
        query = 'lookup' + suffix
        lookup = 'overlap' + suffix
        name = 'name' if not suffix else 'requested'
        rows = [
            ('security', 'security', query,
             f'def {query}(connection, {name}):\n    return connection.execute("SELECT name FROM users WHERE name = \'" + {name} + "\'").fetchall()\n',
             f'def {query}(connection, {name}):\n    return connection.execute("SELECT name FROM users WHERE name = ?", ({name},)).fetchall()\n',
             'SQL input must remain data; preserve legitimate query results.',
             f'''import sqlite3, unittest
from collection_ops import {query}
class Behavior(unittest.TestCase):
 def test_normal(self):
  c=sqlite3.connect(':memory:'); c.execute('CREATE TABLE users(name TEXT)'); c.execute("INSERT INTO users VALUES ('Alice')")
  self.assertEqual({query}(c,'Alice'), [('Alice',)])
 def test_attack(self):
  c=sqlite3.connect(':memory:'); c.execute('CREATE TABLE users(name TEXT)'); c.execute("INSERT INTO users VALUES ('Alice')")
  self.assertEqual({query}(c,"' OR 1=1 --"), [])
'''),
            ('performance', 'performance', lookup,
             f'def {lookup}(left, right):\n    """Both arguments are lists of integers; preserve left order and duplicates."""\n    return [value for value in left if value in right]\n',
             f'def {lookup}(left, right):\n    """Both arguments are lists of integers; preserve left order and duplicates."""\n    members = set(right)\n    return [value for value in left if value in members]\n',
             'Build membership set once under explicit integer-only contract; preserve order/duplicates.',
             f'import unittest\nfrom collection_ops import {lookup}\nclass Behavior(unittest.TestCase):\n def test_values(self): self.assertEqual({lookup}([2,1,2,3],[2,2]), [2,2])\n def test_empty(self): self.assertEqual({lookup}([],[]), [])\n'),
            ('style', 'style', 'format' + suffix,
             f'def format{suffix}(list):\n    Final_Result = ",".join(list)\n    return Final_Result\n',
             f'def format{suffix}(values):\n    result = ",".join(values)\n    return result\n',
             'Human convention rubric: avoid shadowing builtin list and use snake_case local names; public rename needs direction.',
             f'import unittest\nfrom collection_ops import format{suffix}\nclass Behavior(unittest.TestCase):\n def test_values(self): self.assertEqual(format{suffix}(["a","b"]), "a,b")\n'),
            ('test_gap', 'test_gap', 'first' + suffix,
             f'def first{suffix}(values):\n    """Return None for empty input; otherwise the first element."""\n    return values[0] if values else None\n',
             f'def first{suffix}(values):\n    """Return None for empty input; otherwise the first element."""\n    return values[0] if values else None\n',
             'Add explicit empty-input characterization; seeded mutant returns 0 instead of None.',
             f'import unittest\nfrom collection_ops import first{suffix}\nclass Behavior(unittest.TestCase):\n def test_nonempty(self): self.assertEqual(first{suffix}([3,4]),3)\n def test_empty(self): self.assertIsNone(first{suffix}([]))\n'),
            ('dependency', 'test_gap', 'checked' + suffix,
             f'def checked{suffix}(items, allowed):\n    """Membership accepts nested lists; preserve their equality behavior."""\n    return [item for item in items if item in allowed]\n',
             f'def checked{suffix}(items, allowed):\n    """Membership accepts nested lists; preserve their equality behavior."""\n    return [item for item in items if item in allowed]\n',
             'Characterize nested-list behavior before any set refactor; do not assume hashability.',
             f'import unittest\nfrom collection_ops import checked{suffix}\nclass Behavior(unittest.TestCase):\n def test_nested(self): self.assertEqual(checked{suffix}([[1]],[[1]]), [[1]])\n'),
            ('conflict', 'security', 'cached' + suffix,
             f'cache = {{}}\ndef cached{suffix}(tenant, key, fetch):\n    """Different tenants may have different values for the same key."""\n    if key not in cache:\n        cache[key] = fetch(tenant, key)\n    return cache[key]\n',
             f'cache = {{}}\ndef cached{suffix}(tenant, key, fetch):\n    """Different tenants may have different values for the same key."""\n    identity = (tenant, key)\n    if identity not in cache:\n        cache[identity] = fetch(tenant, key)\n    return cache[identity]\n',
             'Tenant isolation overrides cache speed; scope cache key to tenant.',
             f'import unittest\nfrom collection_ops import cached{suffix}, cache\nclass Behavior(unittest.TestCase):\n def test_tenants(self):\n  cache.clear(); fetch=lambda tenant,key:tenant\n  self.assertEqual(cached{suffix}("a",1,fetch),"a")\n  self.assertEqual(cached{suffix}("b",1,fetch),"b")\n')]
        for family, category, symbol, source, corrected, rationale, tests in rows:
            # Test snapshots are explicit. Labels/corrections/hidden assertions never enter model input.
            visible = tests if family not in {'test_gap', 'dependency'} else (
                tests.split(' def test_empty')[0] if family == 'test_gap' else '# No tests supplied in this bounded snapshot.\n')
            cases.append(dict(id=family+suffix, split=split, family=family, source=source,
                visible_tests=visible, corrected=corrected, hidden_tests=tests,
                labels=[dict(category=category, symbol=symbol)], rationale=rationale,
                change_kind='intentional_fix' if family in {'security','conflict'} else 'behavior_preserving',
                required_dependency='characterize_before_refactor' if family == 'dependency' else None))
    controls = [
        ('clean_sql', 'def lookup(connection, name):\n    return connection.execute("SELECT name FROM users WHERE name = ?", (name,)).fetchall()\n'),
        ('clean_lookup', 'def overlap(left, right):\n    """Inputs are integer lists."""\n    members = set(right)\n    return [value for value in left if value in members]\n'),
        ('clean_style', 'def join_names(names):\n    return ",".join(names)\n'),
        ('clean_boundary', 'def first(values):\n    return values[0] if values else None\n')]
    for identity, source in controls:
        # Controls contain adequate visible characterization, including the boundary control.
        tests = {
            'clean_sql': rows[0][-1].replace(query, 'lookup'),
            'clean_lookup': 'import unittest\nfrom collection_ops import overlap\nclass Behavior(unittest.TestCase):\n def test_values(self): self.assertEqual(overlap([2,1,2],[2]), [2,2])\n def test_empty(self): self.assertEqual(overlap([],[]), [])\n',
            'clean_style': 'import unittest\nfrom collection_ops import join_names\nclass Behavior(unittest.TestCase):\n def test_values(self): self.assertEqual(join_names(["a","b"]), "a,b")\n def test_empty(self): self.assertEqual(join_names([]), "")\n',
            'clean_boundary': 'import unittest\nfrom collection_ops import first\nclass Behavior(unittest.TestCase):\n def test_nonempty(self): self.assertEqual(first([3,4]),3)\n def test_empty(self): self.assertIsNone(first([]))\n'}[identity]
        cases.append(dict(id=identity, split='control', family='control', source=source,
            visible_tests=tests, corrected=source, hidden_tests=tests, labels=[],
            rationale='Clean negative control under the stated bounded contract.',
            change_kind='behavior_preserving', required_dependency=None))
    manifest = {'schema': 1, 'seed': 505, 'freeze_note': 'Frozen before first model evaluation; no held-out tuning.', 'cases': cases}
    raw = (json.dumps(manifest, indent=2) + '\n').encode()
    target = HERE / 'manifest.json'
    if target.exists():
        raise ValueError('Frozen corpus already exists; do not overwrite labels')
    target.write_bytes(raw)
    (HERE / 'manifest.sha256').write_text(hashlib.sha256(raw).hexdigest() + '\n')
    print('Frozen', len(cases), 'cases:', hashlib.sha256(raw).hexdigest())


if __name__ == '__main__':
    build()
