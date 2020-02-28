import lexer

########################################
# Test Abstract Syntax Tree
########################################
lexer = lexer.Lexer("1+2+3")
tokens = lexer.make_tokens()
lexer.setTokens(tokens)
ast = lexer.generate_ast()
print(ast.preorderTraversal(ast))
########################################
# End Test Abstract Syntax Tree
########################################
