import pytest
import expression

wrong_exprs = ['f(x)=5^x', 'xx', 'y', 'aa\'', '', 'x^^2', '^2x', 'y(x)=5', 'x%5', '.', '11!']

def wrong_exception_test(expr):
    with pytest.raises(Exception):
        tmp = expression.Expression(expr, -10, 10)
        tmp.eval_expression()       # needed as the ast doesn't start before evaluation

for expr in wrong_exprs:
    wrong_exception_test(expr)

############################################

wrong_evals_exprs = {'x/(x-5)': (0, 10),
        'x*x/x': (-5, 5),
        'x/x': (-5, 5),
        '(x^2+x+5)/x^2': (-5, 5),
        'x': (5, -5),
        '-1': (5, -5),
        'x^2': (5, -5),
        'x^2': (10, 10)}

def wrong_evals_exprs_test(expr, v1, v2):
    with pytest.raises(Exception):
        tmp = expression.Expression(expr, v1, v2)
        tmp.eval_expression()

for expr, (v1, v2) in wrong_evals_exprs.items():
    wrong_evals_exprs_test(expr, v1, v2)

############################################


correct_exprs = {'x^2+x+10': (0, 10, 0**2+0+10),
        'x*x/x': (10, 20, 10*10/10),
        'x^3' : (-5, 5, -5*-5*-5),
        '(x^2+x+5)/x^2': (10, 20, (10**2+10+5)/10**2),
        'x': (-5, 5, -5),
        '-1': (-5, 5, -1),
        'x^2': (-5, 5, -5*-5)}

def correct_exprs_test(expr, v1, v2, expected):
    print(expr)
    tmp = expression.Expression(expr, v1, v2)
    a = tmp.eval_expression()
    print(a)
    assert (tmp.eval_expression()[0] == (v1, expected))

for expr, (v1, v2, expected) in correct_exprs.items():
    correct_exprs_test(expr, v1, v2, expected)

