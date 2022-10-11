from typing import List, Tuple, Union


# Abstraction

def x_is_in_expr(expr: Tuple[str], x: str):
    for subexpr in expr:
        if isinstance(subexpr, tuple) and x_is_in_expr(expr=subexpr, x=x):
            return True
        if x == subexpr:
            return True
    return False


def abstract(expr: Tuple[str], x: str):
    # Strip away outer tuple if it only contains a single tuple
    if len(expr) == 1 and isinstance(expr[0], tuple):
        expr = expr[0]

    if len(expr) == 1 and isinstance(expr[0], str) and expr[0] == x:
        return 'I',
    elif not x_is_in_expr(expr, x):
        return 'K', expr
    else:
        left_expr = expr[:-1]
        left_abstraction = abstract(expr=left_expr, x=x)
        right_expr = expr[-1:]
        right_abstraction = abstract(expr=right_expr, x=x)
        if len(left_abstraction) == 0 or right_abstraction == 0:
            print(1)
        return (('S', left_abstraction), right_abstraction)


not_abstraction_lhs = ('B', 'F', 'T')
not_abstraction = abstract(not_abstraction_lhs, 'B')
assert not_abstraction == (('S', (('S', ('I',)), ('K', ('F',)))), ('K', ('T',)))

or_abstraction_partial = abstract(('B1', 'T', 'B2'), 'B2')
assert or_abstraction_partial == (('S', ('K', ('B1', 'T'))), ('I',))
or_abstraction = abstract(or_abstraction_partial, 'B1')
print('Or Abstraction: ', or_abstraction)


and_abstraction_partial = abstract(('B1', 'B2', 'F'), 'B2')
# assert and_abstraction_partial == ???
and_abstraction = abstract(and_abstraction_partial, 'B1')
print('And Abstraction: ', and_abstraction)
