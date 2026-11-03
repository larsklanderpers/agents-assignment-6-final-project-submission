"""Trusted container-only behavioral and benchmark harness; no target edits."""
import statistics
import time


def run_checks(original, candidate, *, benchmark):
    cases = [([], [1]), ([1], []), ([3, 1, 3, 2], [1, 3, 3]),
             ([[1], [2], [1]], [[1]]), ([1, [2], 3], [[2], 3]),
             ((3, 1, 3), (1, 3)), ([True, 1, False, 0, None], [0, True, None]),
             ([b'a', 'a', None, b'b'], ['a', b'b']), ([1.5, 2.5], [2.5])]
    checks = 0
    for left, right in cases:
        before = repr((left, right))
        expected = original(left, right)
        actual = candidate(left, right)
        assert actual == expected, 'Behavior mismatch: ' + before
        assert repr((left, right)) == before, 'Input mutated'
        checks += 1
    # Fresh generators per invocation preserve the original consumption semantics.
    for factory in (lambda: ((i for i in [1, 3, 1]), [1]),
                    lambda: ([1, 3, 1], (i for i in [1, 3, 1]))):
        assert original(*factory()) == candidate(*factory()), 'Generator behavior changed'
        checks += 1
    def custom(function):
        calls = []
        class Item:
            def __init__(self, value): self.value = value
            def __hash__(self): raise AssertionError('Custom object must not be hashed')
            def __eq__(self, other):
                calls.append((self.value, other.value))
                return self.value == other.value
        result = function([Item(2), Item(1), Item(2)], [Item(1), Item(2)])
        return [v.value for v in result], calls
    assert custom(original) == custom(candidate), 'Custom equality behavior changed'
    checks += 1
    class IntSubclass(int):
        def __hash__(self): raise AssertionError('Subclass must use original loop')
    assert original([IntSubclass(1)], [IntSubclass(1)]) == candidate([IntSubclass(1)], [IntSubclass(1)])
    checks += 1
    metrics = None
    if benchmark:
        left, right = list(range(2500)), list(range(2500))
        assert original(left, right) == candidate(left, right)
        for _ in range(5): original(left, right); candidate(left, right)
        before, after = [], []
        for _ in range(20):
            start = time.perf_counter(); original(left, right); before.append(time.perf_counter() - start)
            start = time.perf_counter(); candidate(left, right); after.append(time.perf_counter() - start)
        metrics = {'kind':'elapsed_time_not_operation_counts', 'size':2500,'warmups':5,'trials':20,
                   'baseline_median_seconds':statistics.median(before),
                   'candidate_median_seconds':statistics.median(after),
                   'baseline_range_seconds':[min(before),max(before)],
                   'candidate_range_seconds':[min(after),max(after)]}
        assert metrics['candidate_median_seconds'] < metrics['baseline_median_seconds'], 'No measured speed improvement'
    return checks, metrics
