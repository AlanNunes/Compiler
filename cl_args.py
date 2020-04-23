# ===========================================================
# = Command Line Arguments =
# ===========================================================
import argparse

def get_args():
    parser = argparse.ArgumentParser(description='AN Compiler')
    parser.add_argument("-src", "--src", metavar='source', help='source code file', required=True)
    parser.add_argument("-dst", "--dst", metavar='destination', help='destination where executable will be created. E.g. \"path\\filename\" or \"filename\"')

    return parser.parse_args()