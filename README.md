# This is a Compiler
It's the first compiler I write, using Python.

# Grammar
expr	: KEYWORD:declare IDENTIFIER EQ expr\
      : term (PLUS|MINUS) term\
term	: factor (MUL|DIV) factor\
factor	: INT|FLOAT\
power	: factor ^ factor

# Requirements
Python version >= 3 ([install python](https://www.python.org/downloads))

# Instructions
Run "main.py" file and then type an expression or something included in the [Grammar](#grammar). The result will be displayed as output.

![Sample](https://i.imgur.com/AFa2wcH.png)
