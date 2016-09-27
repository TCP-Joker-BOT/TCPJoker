#!/usr/bin/env python
"""
Summary:
~~~~~~~~

Evaluate mathematical expressions.
"""

import ast
import math
import fractions
import operator
import multiprocessing


class Calc(ast.NodeVisitor):

    op_map = {
        ast.Add: operator.add,
        ast.BitAnd: operator.and_,
        ast.BitOr: operator.or_,
        ast.BitXor: operator.xor,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.LShift: operator.lshift,
        ast.Mod: operator.mod,
        ast.Mult: operator.mul,
        ast.Pow: operator.pow,
        ast.RShift: operator.rshift,
        ast.Sub: operator.sub,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
        ast.Eq: operator.eq,
        ast.NotEq: operator.ne,
        ast.Lt: operator.lt,
        ast.LtE: operator.le,
        ast.Gt: operator.gt,
        ast.GtE: operator.ge,
        ast.Is: operator.is_,
        ast.IsNot: operator.is_not,
        ast.Not: operator.not_
    }

    func_map = {
        "abs": math.fabs,
        "acos": math.acos,
        "asin": math.asin,
        "atan": math.atan,
        "ceil": math.ceil,
        "cos": math.cos,
        "degrees": math.degrees,
        "radians": math.radians,
        "exp": math.exp,
        "fac": math.factorial,
        "floor": math.ceil,
        "gcd": fractions.gcd,
        "hypot": math.hypot,
        "log": math.log,
        "sin": math.sin,
        "sqrt": math.sqrt,
        "tan": math.tan,
    }

    const_map = {
        "pi": math.pi,
        "e": math.e,
    }

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        try:
            return self.op_map[type(node.op)](left, right)
        except KeyError:
            raise ValueError("operator {} not supported".format(node.op.__class__.__name__))
        except ZeroDivisionError:
            raise ValueError("Division by zero")

    def visit_Name(self, node):
        try:
            return self.const_map[node.id]
        except KeyError:
            raise ValueError("constant {} not supported".format(node.id))

    def visit_Num(self, node):
        return node.n

    def visit_Expr(self, node):
        return self.visit(node.value)

    def visit_UnaryOp(self, node):
        right = self.visit(node.operand)
        try:
            return self.op_map[type(node.op)](right)
        except KeyError:
            raise ValueError("operator {} not supported".format(node.op.__class__.__name__))

    def visit_Call(self, node):
        args = [self.visit(arg) for arg in node.args]
        try:
            return self.func_map[node.func.id](*args)
        except KeyError:
            raise ValueError("function {} not supported" .format(node.func.id))

    def visit_Compare(self, node):
        left = self.visit(node.left)
        out = True
        for op, rnode in zip(node.ops, node.comparators):
            right = self.visit(rnode)
            out = self.op_map[type(op)](left, right)
            left = right
            if not out:
                break
        return out

    @classmethod
    def evaluate(cls, expression):
        tree = ast.parse(expression)
        calc = cls()
        return calc.visit(tree.body[0])


def run(message):
    try:
        pool = multiprocessing.Pool(processes=1)
        async_result = pool.apply_async(Calc.evaluate, (message['text'].split(' ', 1)[1],), {})
        r = str(async_result.get(0.5))
        if len(r) > 100:
            return "Result too long"
        return r
    except ValueError as e:
        return "Error: {}".format(e)
    except MemoryError, RuntimeError:
        return "How kawaii!\nAre you trying to be a cute loli hacker? nyan~"
    except multiprocessing.context.TimeoutError:
        return "Evaluation timeout."
