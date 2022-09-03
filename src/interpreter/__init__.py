
from __future__ import annotations

from compiler.ast_ import Equation, BinOp, UnaryOp, Function, Variable, Number, NodeVisitor
from .unit import Unit, Integer, Ratio, Variable as Var


class Interpreter(NodeVisitor):
    def generic_visit(self, node):
        return super().generic_visit(node)
    
    def interpret(self, tree, namespace: dict[str, Unit] = None):
        self.equation = False
        self.namespace = namespace or {}
        returned = self.visit(tree)
        if not self.equation:
            return returned
        else:
            return Equation(tree.op, *returned)
    
    def visit_equation(self, node: Equation):
        self.equation = True
        left = self.visit(node.left)
        right = self.visit(node.right)
        return left, right
    
    def visit_bin_op(self, node: BinOp):
        op = node.op.value
        left = self.visit(node.left)
        right = self.visit(node.right)

        if op == '+':
            return left + right
        if op == '-':
            return left - right
        if op in {'*', '.'}:
            return left * right
        if op in '//':
            return left / right
        if op == '**':
            return left ** right
    
    def visit_unary_op(self, node: UnaryOp):
        op = node.op.value
        right = self.visit(node.right)

        if op == '+':
            return +right
        if op == '-':
            return -right
    
    def visit_function(self, node: Function):
        name = node.name.value
        func = self.namespace[name]
        val = self.visit(node.expr)
        return func(val)
    
    def visit_variable(self, node: Variable):
        name = node.name.value
        var = self.namespace.get(name, Var(name, 1))
        if type(var) is not Var:
            var = Integer(var)
        return var
    
    def visit_number(self, node: Number):
        val = int(node.value.value)
        return Integer(val)

