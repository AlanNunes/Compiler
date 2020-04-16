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
T_WHILE = 'T_WHILE'
T_ENDWHILE = 'T_ENDWHILE'
T_LOOP = 'T_LOOP'
T_ENDLOOP = 'T_ENDLOOP'
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
T_SEMICOLON = 'T_SEMICOLON'
T_COMMA = 'T_COMMA'
T_AND = 'T_AND'
T_OR = 'T_OR'
T_EOF = 'T_EOF'
T_PRINT = 'T_PRINT'
T_L_BRACKET = 'T_L_BRACKET'
T_R_BRACKET = 'T_R_BRACKET'
T_COLLECTION = 'T_COLLECTION'
T_COLLECTION_ACCESS = 'T_COLLECTION_ACCESS'
T_INDEX = 'T_INDEX'
T_DOT = 'T_DOT'
T_COUNT = 'T_COUNT'
T_APPEND = 'T_APPEND'
T_FUNCTION = 'T_FUNCTION'
T_ENDFUN = 'T_ENDFUN'
T_RETURN = 'T_RETURN'


keywords = [{'declare': T_DECLARE}, {'if': T_IF}, {'else': T_ELSE}, {'elseif': T_ELSEIF}, {'endif': T_ENDIF}, {'and': T_AND}, {'or': T_OR}, {'==': T_EQUALITY}, {'while': T_WHILE}, {'endwhile': T_ENDWHILE}, {'loop': T_LOOP}, {'endloop': T_ENDLOOP}, {'print': T_PRINT}, {'count': T_COUNT}, {'append': T_APPEND}, {'function': T_FUNCTION}, {'endfunction': T_ENDFUN}, {'return': T_RETURN}]
letters = string.ascii_letters

operators = (T_PLUS, T_MINUS, T_MUL, T_DIV, T_POW)
operands = (T_INT, T_FLOAT)
expression = (operators + operands, T_LPARAN, T_RPARAN)

# List of built-in procedures
builtInProc = [T_COUNT, T_APPEND]