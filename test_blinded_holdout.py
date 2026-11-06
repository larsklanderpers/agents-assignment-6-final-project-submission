import unittest
from evaluation.blinded_holdout import check_public, count_findings


class HoldoutTests(unittest.TestCase):
    def case(self):
        return {'id': 'case-01', 'files': {'subject.py': {'role': 'source', 'content': 'def f(x):\n    return x\n'},
                'tests/test_visible.py': {'role': 'test', 'content': 'import unittest\n'}}, 'contracts': {'behavior': 'Return input'}}

    def finding(self, category='security'):
        return {'category': category, 'path': 'subject.py', 'line': 2}

    def test_answer_fields_rejected_from_public_input(self):
        cases = [{**self.case(), 'id': f'case-{i:02}'} for i in range(12)]
        check_public({'schema': 1, 'cases': cases})
        cases[0]['labels'] = []
        with self.assertRaises(ValueError): check_public({'schema': 1, 'cases': cases})

    def test_hidden_file_rejected(self):
        cases = [{**self.case(), 'id': f'case-{i:02}'} for i in range(12)]
        cases[0]['files']['answers.py'] = {'role': 'source', 'content': ''}
        with self.assertRaises(ValueError): check_public({'schema': 1, 'cases': cases})

    def test_duplicates_are_false_positives(self):
        labels = [{'category': 'security', 'path': 'subject.py', 'symbol': 'f'}]
        counts, _ = count_findings(self.case(), labels, [self.finding(), self.finding()])
        self.assertEqual(counts['security'], {'tp': 1, 'fp': 1, 'fn': 0})
        self.assertEqual(len(labels), 1)

    def test_missing_review_counts_all_labels_as_missed(self):
        labels = [{'category': 'security', 'path': 'subject.py', 'symbol': 'f'}]
        counts, _ = count_findings(self.case(), labels, [])
        self.assertEqual(counts['security'], {'tp': 0, 'fp': 0, 'fn': 1})

    def test_wrong_category_does_not_match(self):
        labels = [{'category': 'security', 'path': 'subject.py', 'symbol': 'f'}]
        counts, _ = count_findings(self.case(), labels, [self.finding('style')])
        self.assertEqual(counts['style']['fp'], 1)
        self.assertEqual(counts['security']['fn'], 1)


if __name__ == '__main__': unittest.main()
