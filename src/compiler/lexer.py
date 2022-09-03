
import re
from typing import NamedTuple


class Token(NamedTuple):
    type: str
    value: str
    index: int

    def of(self, *types: str) -> bool:
        return self.type in types


class Lexer:
    def __init__(self, pattern: str) -> None:
        self.pattern = re.compile(pattern, re.DOTALL)

    def error(self, val, idx):
        raise SyntaxError(
            "invalid letter %r at index %i" %(val, idx)
        )

    def eval(self, expr: str):
        i = 0
        while True:
            m = self.pattern.match(expr, i)
            type_ = m.lastgroup.upper()
            val = m.group()

            if type_ == 'MISMATCH':
                self.error(val, i)
            
            if type_ != 'WHITE_SPACE':
                yield Token(type_, val, i)

            if type_ == 'EOL':
                return
            
            i += len(val)
