import string

digits = '.0123456789'

T_INT = 'T_INT'
T_FLOAT = 'T_FLOAT'
T_STRING = 'T_STRING'
T_PLUS = 'T_PLUS'
T_MINUS = 'T_MINUS'
T_DIV = 'T_DIV'
T_MUL = 'T_MUL'
T_POW = 'T_POWER'
T_LPARAN = 'LPARAN'
T_RPARAN = 'RPARAN'
T_DECLARE = 'T_DECLARE'
T_IDENTIFIER = 'T_IDENTIFIER'
T_EQ = 'T_EQ'
T_NOT_INITIALIZED = 'T_NOT_INITIALIZED'
T_IF = 'T_IF'
T_ELSE = 'T_ELSE'
T_ELSEIF = 'T_ELSEIF'
T_ENDIF = 'T_ENDIF'
# Greater Than
T_GT = 'T_GT'
# Less Than
T_LT = 'T_LT'
# Greater Than or Equal
T_GTEQ = 'T_GTEQ'
# Less Than or Equal
T_LTEQ = 'T_LTEQ'
# Equality "=="
T_EQUALITY = 'T_EQUALITY'
T_COLON = 'T_COLON'

keywords = [{'declare': T_DECLARE}, {'if': T_IF}, {'else': T_ELSE}, {'endif': T_ENDIF}]
letters = string.ascii_letters

operators = (T_PLUS, T_MINUS, T_MUL, T_DIV, T_POW)
operands = (T_INT, T_FLOAT)
expression = (operators + operands, T_LPARAN, T_RPARAN)