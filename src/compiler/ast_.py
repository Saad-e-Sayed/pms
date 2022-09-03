
import abc
from dataclasses import dataclass

from .lexer import Token


class AST:
    pass


@dataclass
class BinOp(AST):
    op: Token
    left: AST
    right: AST

@dataclass
class UnaryOp(AST):
    op: Token
    right: AST

@dataclass
class Variable(AST):
    name: Token

@dataclass
class Number(AST):
    value: Token

@dataclass
class Function(AST):
    name: Token
    expr: AST

@dataclass
class Equation(AST):
    op: Token
    left: AST
    right: AST



def _camel_to_snake(name: str) -> str:
    return ''.join((
        '_' + c.lower() if c.isupper() else c
        for c in name
    ))


class NodeVisitor(abc.ABC):
    def visit(self, node: AST, *args, **kws):
        return getattr(self, 'visit' + _camel_to_snake(node.__class__.__name__), self.generic_visit)(node, *args, **kws)
    
    @abc.abstractmethod
    def generic_visit(self, node):
        pass