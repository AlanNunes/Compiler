digits = '.0123456789'

T_INT = 'T_INT'
T_FLOAT = 'T_FLOAT'
T_PLUS = 'T_PLUS'
T_MINUS = 'T_MINUS'
T_DIV = 'T_DIV'
T_MUL = 'T_MUL'
T_POW = 'T_POWER'
T_LPARAN = 'LPARAN'
T_RPARAN = 'RPARAN'

operators = (T_PLUS, T_MINUS, T_MUL, T_DIV, T_POW)
operands = (T_INT, T_FLOAT)
expression = (operators + operands, T_LPARAN, T_RPARAN)
