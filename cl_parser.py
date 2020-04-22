# ===========================================================
# =                   Command Line Parser                   =
# ===========================================================
import argparse


parser = argparse.ArgumentParser(description='AN Compiler')
parser.add_argument("--src", metavar='src', help='source code file')
parser.add_argument("--dst", metavar='dstn', help='destination')

args = parser.parse_args()
print(args)