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
    contents = f.read()
    tokens = lexer.run(contents)
    # =======================================================
    # = Parser                                              =
    # =======================================================
    parser = Parser(tokens)
    ast = parser.parse()

    # =======================================================
    # = Code Generation                                     =
    # =======================================================
    if not parser.error:
        print("***The output compiltation will be generated in ""obj"" folder***")
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
    if not parser.error:
        print("***Runtime execution***")
        interpreter = Interpreter(None)
        result = interpreter.visit(ast)
        print(result)