"""Static literal examples for the bounded Common_Items contract; never run tests.

This checks concrete assertEqual examples against the documented order-preserving
membership contract. It is not a general Python evaluator or a proof of coverage.
Dynamic examples are rejected for human review, not executed during preparation.
"""
import ast


def validate_collection_examples(content):
    if len(content.encode('utf-8')) > 32768:
        raise ValueError('Test proposal exceeds the bounded size')
    tree = ast.parse(content)
    checked = []

    def literal(node, values):
        if isinstance(node, ast.Name) and node.id in values:
            return values[node.id]
        try:
            return ast.literal_eval(node)
        except (ValueError, TypeError, SyntaxError, RecursionError):
            raise ValueError('Collection example must use literal inputs and expectation') from None

    for method in (n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name.startswith('test')):
        values = {}
        for statement in method.body:
            if isinstance(statement, ast.Assign):
                for target in statement.targets:
                    if isinstance(target, ast.Name):
                        values.pop(target.id, None)
                        try:
                            values[target.id] = literal(statement.value, values)
                        except ValueError:
                            pass
            # Only straight-line examples are supported; no branches or helper execution.
            if not isinstance(statement, ast.Expr) or not isinstance(statement.value, ast.Call):
                continue
            assertion = statement.value
            if not (isinstance(assertion.func, ast.Attribute) and assertion.func.attr == 'assertEqual'
                    and len(assertion.args) >= 2):
                values.clear()  # An unsupported call may mutate previously bound inputs.
                continue
            call = assertion.args[0]
            if not (isinstance(call, ast.Call) and isinstance(call.func, ast.Name) and call.func.id == 'Common_Items'):
                values.clear()
                continue
            if len(call.args) != 2 or call.keywords:
                raise ValueError('Collection example requires two positional literal inputs')
            left, right = (literal(node, values) for node in call.args)
            if type(left) not in (list, tuple) or type(right) not in (list, tuple) or max(len(left), len(right)) > 256:
                raise ValueError('Static collection examples require bounded literal lists or tuples')
            expected = literal(assertion.args[1], values)
            # Trusted contract on builtin literal data, not the proposed implementation.
            actual = [item for item in left if item in right]
            if expected != actual:
                raise ValueError(f'{method.name}: expected {expected!r}; membership contract requires {actual!r}')
            checked.append({'test': method.name, 'line': assertion.lineno})
    if not checked:
        raise ValueError('No supported literal Common_Items examples found')
    return {'kind': 'static_literal_membership_contract', 'examples_checked': len(checked),
            'examples': checked, 'test_execution': 'not_run',
            'limitations': 'Straight-line literal assertEqual examples only; not complete test verification.'}
