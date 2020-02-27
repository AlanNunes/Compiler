import lexer
from parser import Parser

while True:
    text = input("Enter code > ")
    tokens = lexer.run(text)
    result = Parser(tokens).parse()
    print(result)
