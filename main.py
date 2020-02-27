import lexer

while True:
    text = input("Enter code > ")
    result = lexer.run(text)
    print(result)