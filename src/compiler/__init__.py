
from .parser_ import Parser
from .lexer import Lexer
from .optimizer import Optimizer


pattern = '|'.join(
    (
        f"(?P<{name}>{regex})" for name, regex in dict(
            # operators
            plus = r'\+',
            minus = '-',
            double_asterisk = r'\*\*',
            asterisk = r'\*',
            double_slash = '//',
            slash = '/',
            equal = '=',
            dot = '\\.',
            # entities
            lparen = r'\(',
            rparen = r'\)',
            num = r'\d+', # only integers are supported for now
            id = r'\w+',
            # others
            white_space = r'\s+',
            eol = '$',
            mismatch = '.',
        ).items()
    )
)

lexer = Lexer(pattern)
tokenize = lexer.eval

parser = Parser()
parse = parser.parse

optimizer = Optimizer()
optimize = optimizer.eval


def compile(expr):
    tokens = lexer.eval(expr)
    ast = parser.parse(tokens)
    units = optimizer.eval(ast)
    return units


if __name__ == '__main__':
    # script for testing purpose
    tokens = lexer.eval("3209.0 + a = b // 5 / sqrt (2)")
    tree = parser.parse(tokens)
    indent = ''
    for c in repr(tree):
        if c == '(':
            print(c)
            indent += ' ' * 4
            print(indent, end='')
        elif c == ')':
            print()
            indent = indent[:-4]
            print(indent, end=c)
        else:
            print(end=c)
    
