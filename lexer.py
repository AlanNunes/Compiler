digits = '0123456789'

T_INT = 'T_INT'
T_PLUS = 'T_PLUS'
T_MINUS = 'T_MINUS'
T_DIV = 'T_DIV'
T_MUL = 'T_MUL'
T_POW = 'T_POWER'
T_LPARAN = 'LPARAN'
T_RPARAN = 'RPARAN'

class Error:
    def __init__(self, name, detail, pos):
        self.name = name
        self.detail = detail
        self.pos = pos

    def raiseError(self):
        print(f"'{self.name}': error ocurred in line {self.pos.ln+1}, col {self.pos.col}: {self.detail}")
        raise SystemExit()

class DividedByZeroError(Error):
    def __init__(self, pos, name = "DividedByZero", detail="You cannot divide a value by zero"):
        self.name = name
        self.detail = detail
        self.pos = pos

class SyntaxError(Error):
    def __init__(self, pos, detail, name = "SyntaxError"):
        self.name = name
        self.detail = detail
        self.pos = pos

class Token:
    def __init__(self, type_, pos, value=None):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        if self.value: return f'{self.type}:{self.value}'
        return f'{self.type}'

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1, self.text)
        self.current_char = None
        self.advance()

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def make_tokens(self):
        tokens = []
        while self.current_char != None:
            if self.current_char in ' \t':
                self.advance()
            elif self.current_char == '+':
                tokens.append(Token(T_PLUS, pos=self.pos))
                self.advance()
            elif self.current_char in digits:
                tokens.append(self.make_number())
            elif self.current_char == '-':
                tokens.append(Token(T_MINUS, pos=self.pos))
                self.advance()
            elif self.current_char == '/':
                tokens.append(Token(T_DIV, pos=self.pos))
                self.advance()
            elif self.current_char == '*':
                tokens.append(Token(T_MUL, pos=self.pos))
                self.advance()
            elif self.current_char == '(':
                tokens.append(Token(T_LPARAN, pos=self.pos))
                self.advance()
            elif self.current_char == ')':
                tokens.append(Token(T_RPARAN, pos=self.pos))
                self.advance()
            elif self.current_char == '-':
                tokens.append(Token(T_MINUS, pos=self.pos))
                self.advance()
            elif self.current_char == '^':
                tokens.append(Token(T_POW, pos=self.pos))
                self.advance()
        return tokens

    def make_number(self):
        num_str = ''
        pos_start = self.pos.copy()
        while self.current_char != None and self.current_char in digits:
            num_str += self.current_char
            self.advance()
        return Token(T_INT, pos=self.pos, value=int(num_str))

class Position:
    def __init__(self, idx, ln, col, text):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.text = text

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.col = 0
            self.ln += 1
        return self

    def copy(self):
        return Position(self.idx, self.ln, self.col, self.text)

#class BinOpNode:
#    def __init__(self, )
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def parse(self):
        return self.parseExpr() if len(self.tokens) > 0 else Error("Empty code", "You can't run empty code", Position(0, 0, 0, "")).raiseError()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]
            return self.current_token
        return
    def parseFactor(self):
        if self.current_token.type == T_INT:
            t = self.current_token.value
            self.advance()
            return t
        elif self.current_token.type == T_LPARAN:
            self.advance()
            t = self.parseExpr()
            self.advance()
            return t
        elif self.current_token.type == T_POW:
            self.advadvance()
            t = self.parsePow()
            self.advance()
            return t
        else:
            SyntaxError(self.current_token.pos, f"Expected a value or expression, but found '{self.current_token}'").raiseError()

    def parseExpr(self):
        fac1 = self.parseTerm()
        while self.current_token.type == T_PLUS or self.current_token.type == T_MINUS:
            if self.current_token.type == T_PLUS:
                self.advance()
                fac2 = self.parseTerm()
                fac1 = fac1 + fac2
            elif self.current_token.type == T_MINUS:
                self.advance()
                fac2 = self.parseTerm()
                fac1 = fac1 - fac2
        return fac1

    def parseTerm(self):
        fac1 = self.parseFactor()
        while self.current_token.type == T_MUL or self.current_token.type == T_DIV or self.current_token.type == T_POW:
            if self.current_token.type == T_MUL:
                self.advance()
                fac2 = self.parseFactor()
                fac1 = fac1 * fac2
            elif self.current_token.type == T_DIV:
                self.advance()
                fac2 = self.parseFactor()
                if fac2 == 0:
                    DividedByZeroError(self.current_token.pos).raiseError()
                fac1 = fac1 / fac2
            elif self.current_token.type == T_POW:
                self.advance()
                if self.current_token.type not in (T_LPARAN, T_INT):
                    Error("Invalid power", "A power operator must be followed by '(' or 'integer'", self.current_token.pos).raiseError()
                fac2 = self.parseFactor()
                fac1 = fac1 ** fac2
        return fac1

def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    parser = Parser(tokens)
    return parser.parse()
