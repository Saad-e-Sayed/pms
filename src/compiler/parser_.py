
from .ast_ import Equation, BinOp, UnaryOp, Variable, Number, Function, Token


class Parser:
    """

    equation: side ('=' side)?
    side: expr ('//' expr)?
    expr: term (('+'|'-') term)*
    term: factor (('*'|'/') factor)*
    factor: chain ('**' chain)*
    chain: preatom ('.' atom)*
    preatom: ('+'|'-')? (NUM | atom)
    atom: var | func | paren
    var: ID
    func: ID paren
    paren: '(' expr ')'
    """
    __slots__ = 'tokens', 'index'

    def error(self, expected, found):
        raise SyntaxError(
            "expected %s but got %r" %(expected, found)
        )

    def peek(self, steps = 0) -> Token:
        return self.tokens[self.index + steps]
    
    def advance(self, steps = 1):
        self.index += steps
        return self
    
    def eat(self, type_: str) -> None:
        token = self.advance().peek()
        if not token.of(type_):
            self.error(type_, token.type)
    
    def parse(self, tokens):
        self.tokens = tuple(tokens)
        self.index = 0
        tree = self._equation()
        self.eat('EOL')
        return tree
    

    def _equation(self):
        side = self._side()
        
        t = self.peek(1)
        if t.of('EQUAL'):
            aside = self.advance(2)._side()
            side = Equation(t, side, aside)
        
        return side
    
    def _side(self):
        expr = self._expr()
        
        t = self.peek(1)
        if t.of('DOUBLE_SLASH'):
            aside = self.advance(2)._expr()
            expr = BinOp(t, expr, aside)
        
        return expr

    def _expr(self):
        term = self._term()

        while self.peek(1).of('PLUS', 'MINUS'):
            op = self.peek(1)
            operand = self.advance(2)._term()
            term = BinOp(op, term, operand)
        
        return term
    
    def _term(self):
        factor = self._factor()

        while self.peek(1).of('ASTERISK', 'SLASH'):
            op = self.peek(1)
            operand = self.advance(2)._factor()
            factor = BinOp(op, factor, operand)
        
        return factor
    
    def _factor(self):
        chain = self._chain()

        while self.peek(1).of('DOUBLE_ASTERISK'):
            op = self.peek(1)
            power = self.advance(2)._chain()
            chain = BinOp(op, chain, power)

        return chain
    
    def _chain(self):
        atom = self._preatom()

        while self.peek(1).of('DOT'):
            op = self.peek(1)
            operand = self.advance(2)._atom()
            atom = BinOp(op, atom, operand)
        
        return atom

    def _preatom(self):
        if x:= self.peek().of('PLUS', 'MINUS'):
            t = self.advance().peek(-1)
        
        if self.peek().of('NUM'):
            atom = Number(self.peek())
        else:
            atom = self._atom()
        
        return UnaryOp(t, atom) if x else atom

    def _atom(self):
        t = self.peek()
        if t.of('ID'):
            if self.peek(1).of('LPAREN'):
                expr = self.advance(2)._expr()
                self.eat('RPAREN')
                return Function(t, expr)
            else:
                return Variable(t)
        elif t.of('LPAREN'):
            expr = self.advance()._expr()
            self.eat('RPAREN')
            return expr
        
        self.error('ID', t.type)

