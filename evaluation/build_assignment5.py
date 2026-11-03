"""Create new development cases from a pinned Assignment 5 snapshot, never edit it."""
import argparse
import hashlib
import json
from pathlib import Path
from repository_intake import validate

SOURCE = 'backend/guardrails/output_filter.py'
VISIBLE = '''import unittest
from backend.guardrails.output_filter import sanitize_output, mask_financial_details
class Visible(unittest.TestCase):
 def test_plain(self): self.assertEqual(sanitize_output('ordinary text'), 'ordinary text')
 def test_amount(self): self.assertEqual(mask_financial_details('Cost $12,345.67'), 'Cost $***5.67')
 def test_ssn(self): self.assertEqual(sanitize_output('SSN 123-45-6789'), 'SSN ***-**-XXXX')
'''
HIDDEN = '''import unittest
from backend.guardrails.output_filter import sanitize_output, mask_financial_details
class Acceptance(unittest.TestCase):
 def test_email(self): self.assertEqual(sanitize_output('Mail a.person@example.test now'), 'Mail [EMAIL REDACTED] now')
 def test_email_second(self): self.assertEqual(sanitize_output('x+y@sample.org'), '[EMAIL REDACTED]')
 def test_account(self): self.assertEqual(mask_financial_details('Account 12345678901'), 'Account *******8901')
 def test_account_boundary(self): self.assertEqual(mask_financial_details('12345678'), '****5678')
 def test_short_digits(self): self.assertEqual(mask_financial_details('1234567'), '1234567')
 def test_decimal(self): self.assertEqual(mask_financial_details('$9.50'), '$***9.50')
 def test_integer(self): self.assertEqual(mask_financial_details('$12345'), '$***345')
 def test_phone(self): self.assertEqual(sanitize_output('Call 555-123-4567'), 'Call ***-***-XXXX')
 def test_plain(self): self.assertEqual(sanitize_output('ordinary text'), 'ordinary text')
'''


def build(snapshot, contracts):
    validate(snapshot)
    original = snapshot['files'][SOURCE]['content']
    needle = '        text = pattern.sub(replacements[name], text)'
    if original.count(needle) != 1 or original.count('m.group()[-4:]') != 1:
        raise ValueError('Assignment source changed; review mutations before creating a new corpus')
    cases = []
    for identity, source, symbol, mutation in [
        ('a5-original-control', original, None, None),
        ('a5-email-omission', original.replace(needle, '        if name != "email":\n    ' + needle), 'sanitize_output', 'Skip email masking'),
        ('a5-account-leak', original.replace('m.group()[-4:]', 'm.group()[-6:]'), 'mask_financial_details', 'Expose six trailing account digits instead of four')]:
        cases.append({'id': identity, 'split': 'development', 'source_path': SOURCE,
                      'files': {SOURCE: {'role': 'source', 'content': source},
                                'tests/test_visible.py': {'role': 'test', 'content': VISIBLE}},
                      'contracts': {k: v for k, v in contracts.items() if k in {'pii-redaction', 'financial-mask', 'public-api'}},
                      'hidden_tests': HIDDEN, 'labels': [] if symbol is None else [{'category': 'security', 'symbol': symbol}],
                      'expected': 'no_change' if symbol is None else 'repair', 'seeded_mutation': mutation,
                      'original_source_sha256': hashlib.sha256(original.encode()).hexdigest()})
    return {'schema': 1, 'origin': {'repository': snapshot['repository_name'], 'commit': snapshot['commit'],
                                  'snapshot_sha256': snapshot['snapshot_sha256'], 'path': SOURCE},
            'limitations': ['Development pilot only; not a holdout or a full corpus.',
                'Mutations are intentionally introduced in disposable copies, not discovered defects in Assignment 5.',
                'Acceptance tests are newly authored stdlib tests; they do not claim the original check_ harness ran.',
                'Labels and acceptance contracts require independent human review.'], 'cases': cases}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--snapshot', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    snapshot = json.loads(Path(args.snapshot).read_text(encoding='utf-8'))
    contracts = json.loads(Path(__file__).with_name('assignment5-contracts.json').read_text(encoding='utf-8'))
    payload = json.dumps(build(snapshot, contracts), indent=2).encode()
    target = Path(args.output)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream: stream.write(payload)
    with target.with_suffix('.sha256').open('x') as stream: stream.write(hashlib.sha256(payload).hexdigest() + '\n')
    print(json.dumps({'manifest': str(target), 'cases': 3, 'split': 'development', 'sha256': hashlib.sha256(payload).hexdigest()}))
