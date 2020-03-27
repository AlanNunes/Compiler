import sys
import lexer
from parser_ import Parser, Interpreter

f=open(sys.argv[1], "r")
#f=open("tests/collection.an", "r")
if f.mode == 'r':
    contents = f.read()
    #print (contents)
    tokens = lexer.run(contents)
    #print(tokens)
    ast = Parser(tokens).parse()
    interpreter = Interpreter(None)
    result = interpreter.visit(ast)
    #interpreter.symb_table.print()
    #print(result)