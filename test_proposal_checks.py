"""Regression for the actual generated wrong-order expectation; no code execution."""
import unittest
import difflib
from pathlib import Path
import tempfile
from unittest.mock import patch
from proposal_checks import validate_collection_examples


def example(expected):
    return ('import unittest\nclass Tests(unittest.TestCase):\n'
        ' def test_duplicates(self):\n'
        '  left = [1, 2, 1, 3, 1]\n  right = [1, 3]\n'
        f'  self.assertEqual(Common_Items(left, right), {expected})\n')


class LiteralExampleChecks(unittest.TestCase):
    def test_bad_example_blocks_gate_preparation_before_preflight(self):
        import approval_executor as ae
        root = ae.PROJECT / 'artifacts/tests'
        root.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(dir=root) as name:
            directory = Path(name)
            text = example('[1, 1, 1, 3]')
            diff = ''.join(difflib.unified_diff([], text.splitlines(keepends=True),
                fromfile='/dev/null', tofile='b/' + ae.TARGET))
            (directory / 'candidate.patch').write_bytes(diff.encode())
            with patch.object(ae, 'preflight') as preflight:
                with self.assertRaisesRegex(ValueError, 'membership contract requires'):
                    ae.prepare(directory)
                preflight.assert_not_called()
            self.assertEqual([p.name for p in directory.iterdir()], ['candidate.patch'])

    def test_rejects_observed_model_order_error(self):
        with self.assertRaisesRegex(ValueError, 'membership contract requires'):
            validate_collection_examples(example('[1, 1, 1, 3]'))

    def test_accepts_correct_order_and_nested_unhashable_literals(self):
        self.assertEqual(validate_collection_examples(example('[1, 1, 3, 1]'))['examples_checked'], 1)
        nested = example('[[1], [1]]').replace('[1, 2, 1, 3, 1]', '[[1], [2], [1]]').replace('right = [1, 3]', 'right = [[1]]')
        self.assertEqual(validate_collection_examples(nested)['examples_checked'], 1)

    def test_does_not_evaluate_dynamic_expected_expression(self):
        with self.assertRaisesRegex(ValueError, 'literal inputs and expectation'):
            validate_collection_examples(example('__import__("sys").exit(99)'))

    def test_reports_unsupported_or_missing_examples(self):
        with self.assertRaises(ValueError):
            validate_collection_examples('import unittest\n')
        with self.assertRaises(ValueError):
            validate_collection_examples(example('sorted(left)'))
        mutated = example('[1, 1, 3, 1]').replace('  self.assertEqual', '  left.append(9)\n  self.assertEqual')
        with self.assertRaises(ValueError):
            validate_collection_examples(mutated)


if __name__ == '__main__':
    unittest.main()
