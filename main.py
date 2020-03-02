import lexer
from parser_ import Parser, Interpreter

while True:
    text = input("Enter code > ")
    tokens = lexer.run(text)
    ast = Parser(tokens).parse()
    result = Interpreter(None).visit(ast)
    print(result)