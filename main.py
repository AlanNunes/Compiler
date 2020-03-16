import lexer
from parser_ import Parser, Interpreter

while True:
    text = input("Enter code _> ")
    tokens = lexer.run(text)
    print(tokens)
    ast = Parser(tokens).parse()
    interpreter = Interpreter(None)
    result = interpreter.visit(ast)
    #interpreter.symb_table.print()
    print(result)