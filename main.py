import sys
import os
import lexer
import uuid
from parser_ import Parser
from runtime.interpreter import Interpreter
from code_generator import CSharp

# =======================================================
# = Source Code                                         =
# =======================================================
#f=open(sys.argv[1], "r")
f=open("tests/while.an", "r")
if f.mode == 'r':
    print("*The output compiltation will be generated in ""obj"" folder")
    contents = f.read()
    #print (contents)
    tokens = lexer.run(contents)
    #print(tokens)
    # =======================================================
    # = Parser                                              =
    # =======================================================
    parser = Parser(tokens)
    ast = parser.parse()

    # =======================================================
    # = Code Generation                                     =
    # =======================================================
    code_generator = CSharp(ast, parser.current_symb_tbl)
    res = code_generator.gen_base_structure(ast.stmts)
    if not os.path.exists('obj'):
        os.makedirs('obj')
    obj_f = open(f"obj/output{uuid.uuid1()}.cs","w+")
    obj_f.write(res)
    obj_f.close()

    # =======================================================
    # = Runtime Execution                                   =
    # =======================================================
    interpreter = Interpreter(None)
    result = interpreter.visit(ast)
    print(result)