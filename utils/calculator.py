import ast, operator

def safe_eval(expr: str):
    """
    Safely evaluates a math expression.

    The use of eval is not recommended in prod environments. This function is a safer approach
    for evaluating ONLY math expressions.
    """
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.USub: operator.neg
    }

    def eval_node(node):
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](eval_node(node.left), eval_node(node.right))
        elif isinstance(node, ast.UnaryOp):
            return operators[type[node.op]](eval_node(node.operand))
        elif isinstance(node, ast.Expr):
            return eval_node(node.value)
        else:
            raise TypeError(f"Unsupported node type: {type(node)}")

    result = eval_node(ast.parse(expr, mode = "eval").body)

    if isinstance(result, float):
        return round(result, 2)
    elif isinstance(result, int):
        return result
    else:
        raise RuntimeError(f"Unsupported result type: {type(result)}")
    

def calculate(expression: str) -> float:
    return float(safe_eval(expr=expression))


# TEST CASES

assert (actual := calculate("10 + 7")) == 17.0, f"Expected 17.0, got {actual}"