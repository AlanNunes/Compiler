import sys
import lexer
from parser_ import Parser
from runtime.interpreter import Interpreter
from code_generator import CSharp

#f=open(sys.argv[1], "r")
f=open("tests/parser_symb_tbl.an", "r")
if f.mode == 'r':
    contents = f.read()
    #print (contents)
    tokens = lexer.run(contents)
    #print(tokens)
    parser = Parser(tokens)
    ast = parser.parse()
    code_generator = CSharp(ast, parser.current_symb_tbl)
    res = code_generator.gen_stmts(ast.stmts)
    print(res)
    print("Done")
    #interpreter = Interpreter(None)
    #result = interpreter.visit(ast)
    #print(interpreter.current_symbTbl)
    #print(result)