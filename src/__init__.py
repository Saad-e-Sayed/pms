
from compiler import lexer, parser
from interpreter import Interpreter


tree = parser.parse(lexer.eval('a = 5 / b'))

print(Interpreter().interpret(tree, {'b':3}))