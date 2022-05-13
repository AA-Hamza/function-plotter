import ast
import operator as op
import numpy as np

_OPERATORS = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Pow: op.pow, ast.USub: op.neg}
_MAX_STEP_INVERSE = 100
_VALID_EXPR_SYMBOLS = {'1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '+', '-', '/', '*', '^', 'x'}

# it should be safe as we aren't using eval
# I definetly would have taken a different route if I had the time
class Expression:
    """
        A class to calculate a mathematical formula 
        taking advantage of Python's built in Abstract Syntax Tree library
    """
    def __init__(self, expr:str, start:float, end:float):
        self.expr = expr.replace("^", "**")      # Translate ^ to ** (Python's pow), needed for ast.Pow
        # basic validation, not really needed, gives a better error message
        for char in expr:
            if char not in _VALID_EXPR_SYMBOLS:
                raise Exception("Unrecognized symbol: "+char)

        # If python couldn't parse it
        try:
            self.tree_root = ast.parse(expr, mode='eval')
        except:
            raise Exception("Invalid Equation")

        self.start = start
        self.end = end
        # Just making sure that step doesn't get out of hand
        self.step = max(_MAX_STEP_INVERSE**-1, (self.end-self.start)/_MAX_STEP_INVERSE)

    def eval_expression(self):
        num_of_elements = int((self.end-self.start)//self.step)
        arr = np.empty(shape=(num_of_elements, 2), dtype=float)
        index = 0
        _start = self.start
        while (index < num_of_elements): 
            arr[index] = _start, self._eval_expression(self.tree_root.body, _start)
            index += 1
            _start += self.step
        return arr

    def _eval_expression(self, node, x):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            if type(node.op) not in _OPERATORS:
                raise Exception("Unsupported operation")
            return _OPERATORS[type(node.op)](
                self._eval_expression(node.left, x),
                self._eval_expression(node.right, x))

        elif isinstance(node, ast.UnaryOp):
            if (type(node.op) not in _OPERATORS):
                raise Exception("Unsupported operation")
            return _OPERATORS[type(node.op)](
                self._eval_expression(node.operand, x))

        elif isinstance(node, ast.Name):
            if (node.id != 'x'):
                raise Exception("Unrecognized symbol: "+node.id)
            return x
        else:
            raise Exception("Unknown Error")
