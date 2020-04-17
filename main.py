import sys
import os
import lexer
import uuid
import time
import msgs_log
from parser_ import Parser
from runtime.interpreter import Interpreter
from code_generator import CSharp
from ast import AST

# =======================================================
# =                    Source Code                      =
# =======================================================
#f=open(sys.argv[1], "r")
f=open("tests/fibonacci.an", "r")
if f.mode == 'r':
    # =======================================================
    # =                      Lexer                          =
    # =======================================================
    msgs_log.print_title("Doing Lexer")
    start = time.time()
    contents = f.read()
    tokens = lexer.run(contents)
    end = time.time()
    print("Time execution: " + str(end - start) + "ms")
    # =======================================================
    # =                     Parser                          =
    # =======================================================
    msgs_log.print_title("Doing Parser")
    start = time.time()
    parser = Parser(tokens)
    ast = parser.parse()
    end = time.time()
    print("Time execution: " + str(end - start) + "ms")

    # =======================================================
    # =                 Code Generation                     =
    # =======================================================
    if not parser.error:
        msgs_log.print_title("Doing Code Generator")
        start = time.time()
        code_generator = CSharp(ast, parser.current_symb_tbl)
        res = code_generator.gen_base_structure(ast.stmts)
        if not os.path.exists('obj'):
            os.makedirs('obj')
        f_name = f"obj/output{uuid.uuid1()}.cs"
        obj_f = open(f_name,"w+")
        obj_f.write(res)
        obj_f.close()
        end = time.time()
        print(f"*Output: '{f_name}'")
        print("Time execution: " + str(end - start) + "ms")

    # =======================================================
    # =                 Runtime Execution                   =
    # =======================================================
    if not parser.error:
        start = time.time()
        msgs_log.print_title("Runtime execution")
        interpreter = Interpreter(None)
        interpreter.visit(ast)
        end = time.time()
        print("Time execution: " + str(end - start) + "ms")

    ast2 = AST(ast, parser.current_symb_tbl)
    ast2.print()