import sys
import os
import lexer
import uuid
import time
import msgs_log
import prepare_compiler
import cl_args
from parser_ import Parser
from runtime.interpreter import Interpreter
from code_generator import CSharp
from ast import AST

# Welcome
msgs_log.print_welcome("Welcome to AN Compiler!", "\"it's easier to ask forgiveness than it is to get permission\"", "Contribute here: https://github.com/AlanNunes/Compiler", "Author: Alan Nunes da Silva (alann.625@gmail.com)", "Version 1.0 (2020)")

# Get command line arguments
#args = cl_args.get_args()
class Arg:
    src = "tests\procedure.an"
    dst = None

args = Arg()

# Prepare Compiler Environment
prepare_compiler.load_csharp_environment()

# Open source code
f=open(args.src, "r")
if f.mode == 'r':
    # =======================================================
    # =                      Lexer                          =
    # =======================================================
    msgs_log.print_title("Doing Lexer")
    start = time.time()
    contents = f.read()
    tokens = lexer.run(contents)
    end = time.time()
    print("Execution time: " + str(end - start) + "ms")
    # =======================================================
    # =                     Parser                          =
    # =======================================================
    msgs_log.print_title("Doing Parser")
    start = time.time()
    parser = Parser(tokens)
    ast = parser.parse()
    end = time.time()
    print("Execution time: " + str(end - start) + "ms")

    # =======================================================
    # =                CSharp Code Generation               =
    # =======================================================
    if not parser.error:
        msgs_log.print_title("Doing Code Generator (C#)")
        start = time.time()
        code_generator = CSharp(ast, parser.current_symb_tbl)
        res = code_generator.gen_base_structure(ast.stmts)
        if not os.path.exists('obj'):
            os.makedirs('obj')
        if args.dst:
            f_name = f"{args.dst}.cs"
        else:
            f_name = os.path.basename(args.src)
            f_name = f"{os.getcwd()}\obj\{f_name}.cs"
        obj_f = open(f_name,"w+")
        obj_f.write(res)
        obj_f.close()
        end = time.time()
        print(f"*Output: '{f_name}'")
        print("Execution time: " + str(end - start) + "ms")


    # =======================================================
    # =               CSharp Compiltation                   =
    # =======================================================
    msgs_log.print_title("Doing CSharp Compilation")
    start = time.time()
    csc = os.environ['CSharpComp']
    src = os.path.splitext(f_name)[0]
    dst = args.dst if args.dst else f"{f_name}"
    os.system(f'{csc}/csc -optimize /nologo -out:\"{dst}.exe\" \"{src}.cs\"')
    end = time.time()
    print(f"*Output: '{src}.exe'")
    print("Execution time: " + str(end - start) + "ms")


    # =======================================================
    # =                 RunExecution time                   =
    # =======================================================
    if not parser.error:
        start = time.time()
        msgs_log.print_title("Runtime")
        interpreter = Interpreter(None)
        interpreter.visit(ast)
        end = time.time()
        print("Execution time: " + str(end - start) + "ms")

    ast2 = AST(ast, parser.current_symb_tbl)
    ast2.print()