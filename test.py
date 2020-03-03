import lexer
from parser_ import Parser, Interpreter

text = "2^3"
tokens = lexer.run(text)
parser = Parser(tokens).parse()
interpreter = Interpreter(None)
result = interpreter.visit(parser)
print(result)