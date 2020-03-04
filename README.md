# This is a Compiler
It's the first compiler I write. I am building a new own programming language.

# Grammar
variable   : KEYWORD IDENTIFIER EQ expr\
               : IDENTIFIER EQ expr\
               : KEYWORD IDENTIFIER\
expr	       : KEYWORD:declare IDENTIFIER EQ expr\
               : term (PLUS|MINUS) term\
term        : factor (MUL|DIV) factor\
factor		    	: INT|FLOAT|IDENTIFIER\
power	    : factor ^ factor

# Requirements
Python version >= 3 ([install python](https://www.python.org/downloads))

# Instructions
Run "main.py" file and then type an expression or something included in the [Grammar](#grammar). The result will be displayed as output.

![Sample](https://i.imgur.com/OtAqG7y.png)


# Contact
E-mail: [alann.625@gmail.com](mailto:alann.625@gmail.com)\
Linkedin: [Alan Nunes](https://www.linkedin.com/in/alan-nunes-848374152)
