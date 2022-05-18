import pytest
import expression

wrong_exprs = ['f(x)=5^x', 'xx', 'y', 'aa\'', '', 'x^^2', '^2x', 'y(x)=5', 'x%5', '.', '11!']

@pytest.mark.parametrize("expr", wrong_exprs)
def test_wrong_exception(expr):
    with pytest.raises(Exception):
        tmp = expression.Expression(expr, -10, 10)
        tmp.eval_expression()       # needed as the ast doesn't start before evaluation
############################################

wrong_evals_exprs = [('x/x', 0, 10), # some times the program gets away with dividing by zero as we don't test all values
        ('x', 5, -5),
        ('-1', 5, -5),
        ('x^2', 5, -5),
        ('x^2', 10, 10)]

@pytest.mark.parametrize("expr,v1,v2", wrong_evals_exprs)
def test_wrong_evals_exprs(expr, v1, v2):
    with pytest.raises(Exception):
        tmp = expression.Expression(expr, v1, v2)
        tmp.eval_expression()

############################################

correct_exprs = [('x^2+x+10', 0, 10, 0**2+0+10),
        ('x*x/x', 10, 20, 10*10/10),
        ('x^3'  ,-5, 5, -5*-5*-5),
        ('(x^2+x+5)/x^2', 10, 20, (10**2+10+5)/10**2),
        ('x', -5, 5, -5),
        ('-1', -5, 5, -1),
        ('x^2', -5, 5, -5*-5)]

@pytest.mark.parametrize("expr,v1,v2,expected", correct_exprs)
def test_correct_exprs(expr, v1, v2, expected):
    print(expr)
    tmp = expression.Expression(expr, v1, v2)
    np_array = tmp.eval_expression()
    assert (np_array[0, 1] == expected)
