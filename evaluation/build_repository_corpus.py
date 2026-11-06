"""Synthetic, author-known multi-module development corpus; not a blinded holdout."""
import argparse
import hashlib
import json
from pathlib import Path

RULES = '''def discount(subtotal, member):
    return subtotal * 10 // 100 if member else 0
'''
SERVICE = '''from pricing.rules import discount

def total(prices, member):
    subtotal = sum(prices)
    return subtotal - discount(subtotal, member)
'''
VISIBLE = '''import unittest
from pricing.service import total
class Visible(unittest.TestCase):
    def test_empty(self): self.assertEqual(total([], False), 0)
    def test_empty_member(self): self.assertEqual(total([], True), 0)
'''
HIDDEN = '''import unittest
from pricing.service import total
from pricing.rules import discount
class Acceptance(unittest.TestCase):
    def test_member(self): self.assertEqual(total([100, 200], True), 270)
    def test_guest(self): self.assertEqual(total([100, 200], False), 300)
    def test_floor(self): self.assertEqual(total([19], True), 18)
    def test_zeros(self): self.assertEqual(total([0, 0], True), 0)
    def test_rule_member(self): self.assertEqual(discount(199, True), 19)
    def test_rule_guest(self): self.assertEqual(discount(199, False), 0)
'''


def build():
    cases = []
    for identity, rules, service, forced in [
        ('clean-multimodule', RULES, SERVICE, False),
        ('discount-defect', RULES.replace('* 10', '* 20'), SERVICE, False),
        ('two-module-defects', RULES.replace('* 10', '* 20'), SERVICE.replace('subtotal -', 'subtotal +'), False),
        ('forced-recovery', RULES, SERVICE.replace('subtotal -', 'subtotal +'), True)]:
        files = {p: {'role': role, 'content': text} for p, role, text in [
            ('pricing/__init__.py', 'source', ''), ('pricing/rules.py', 'source', rules),
            ('pricing/service.py', 'source', service), ('tests/test_visible.py', 'test', VISIBLE)]}
        cases.append({'id': identity, 'files': files, 'contracts': {
            'discount': 'For nonnegative integer subtotal in cents, discount returns floor(subtotal * 10 / 100) for members and zero for guests.',
            'total': 'For a list of nonnegative integer prices in cents, total returns their sum MINUS discount(sum, member). Empty lists return zero.',
            'scope': 'Preserve existing APIs/imports. Test-coverage assessment, style, annotations and performance suggestions are outside this experiment.'},
            'hidden_tests': HIDDEN, 'expected': 'no_change' if identity.startswith('clean') else 'repair',
            'force_failure': forced})
    return {'schema': 1, 'split': 'development', 'cases': cases,
            'limitations': ['Synthetic, author-known cases, no independent adjudication or generalization claim.',
                            'Stdlib unittest only; package installation unsupported.']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(build(), indent=2).encode()
    with args.output.open('xb') as stream: stream.write(payload)
    with args.output.with_suffix('.sha256').open('x') as stream: stream.write(hashlib.sha256(payload).hexdigest())
