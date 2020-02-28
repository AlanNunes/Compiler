from constant import *
from ast import Node


class Token:
    def __init__(self, type_, pos, value=None):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        if self.value:
            return f'{self.type}:{self.value}'
        return f'{self.type}'


class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = Position(-1, 0, -1, self.text)
        self.current_char = None
        self.node = Node()
        self.advance()

    def setTokens(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1

    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = self.text[self.pos.idx] if self.pos.idx < len(self.text) else None

    def advanceTk(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]
            return self.current_token
        return

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
            elif self.current_char in letters:
                tokens.append(self.make_identifier())
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
            elif self.current_char == "=":
                tokens.append(Token(T_EQ, pos=self.pos))
                self.advance()

        return tokens

    def make_number(self):
        pos_start = self.pos.copy()
        num_str = '0'if self.current_char == '.' else ''
        while self.current_char != None and (self.current_char in digits or self.current_char == '.'):
            num_str += self.current_char
            self.advance()
        try:
            int(num_str)
            return Token(T_INT, pos=self.pos, value=int(num_str))
        except:
            return Token(T_FLOAT, pos=self.pos, value=float(num_str))

    def make_identifier(self):
        pos_start = self.pos.copy()
        id = ''
        while self.current_char != None and self.current_char in letters:
            id += self.current_char
            self.advance()
        if id in keywords:
            return Token(T_KEYWORD, pos=self.pos, value=id)
        else:
            return Token(T_IDENTIFIER, pos=self.pos, value=id)

    def generate_ast(self):
        self.advanceTk()
        if len(self.tokens) > 0:
            self.parseExpr()
            return self.node
        return

    def getNextToken(self):
        return self.tokens[self.tok_idx+1] if len(self.tokens) > 0 else None

    def parseFactor(self):
        if self.current_token.type in (T_INT, T_FLOAT):
            t = self.current_token
            self.advanceTk()
            print(f"advanced to {self.current_token}")
            if self.current_token.type in operators:
                nTok = self.getNextToken()
                if nTok != None and nTok.type not in operands + (T_LPARAN,):
                    SyntaxError(self.current_token.pos,
                                f"Expected a '+, -, /, *, ^, (' but found {self.current_token}").raiseError()
            return t
        elif self.current_token.type == T_LPARAN:
            self.advanceTk()
            t = self.parseExpr()
            self.advanceTk()
            return t
        elif self.current_token.type == T_POW:
            self.advanceTk()
            t = self.parsePow()
            self.advanceTk()
            return t
        elif self.current_token.type in (T_KEYWORD, T_IDENTIFIER, T_EQ):
            self.advanceTk()
            t = self.parseExpr()
            self.advanceTk()
            return t
        else:
            SyntaxError(self.current_token.pos,
                        f"Expected a value or expression, but found '{self.current_token}'").raiseError()

    def parseExpr(self):
        fac1 = self.parseTerm()
        while self.current_token.type == T_PLUS or self.current_token.type == T_MINUS:
            if self.current_token.type == T_PLUS:
                self.node.insert(self.current_token)
                self.advanceTk()
                fac2 = self.parseTerm()
                self.node.insert(fac2)
                #fac1 = f"({fac1} + {fac2})"
            elif self.current_token.type == T_MINUS:
                self.node.insert(self.current_token)
                self.advanceTk()
                fac2 = self.parseTerm()
                self.node.insert(fac2)
                #fac1 = f"({fac1} - {fac2})"
        while self.current_token.type == T_KEYWORD:
            self.advanceTk()
            if self.current_token.type != T_IDENTIFIER:
                SyntaxError(
                    pos=self.pos, detail=f"Expected a identifier, but found '{self.current_token}'")
            self.advanceTk()
            if self.current_token.type != T_EQ:
                SyntaxError(
                    pos=self.pos, detail=f"Expected a identifier, but found '{self.current_token}'")
            self.advanceTk()
        self.node.insert(fac1)
        return fac1

    def parseTerm(self):
        fac1 = self.parseFactor()
        while self.current_token.type == T_MUL or self.current_token.type == T_DIV or self.current_token.type == T_POW:
            if self.current_token.type == T_MUL:
                self.node.insert(self.current_token)
                self.advanceTk()
                fac2 = self.parseFactor()
                self.node.insert(fac1)
                self.node.insert(fac2)
                #fac1 = f"({fac1} * {fac2})"
            elif self.current_token.type == T_DIV:
                self.node.insert(self.current_token)
                self.advanceTk()
                fac2 = self.parseFactor()
                self.node.insert(fac1)
                self.node.insert(fac2)
                if fac2 == 0:
                    DividedByZeroError(self.current_token.pos).raiseError()
                #fac1 = f"({ac1} / {fac2})"
            elif self.current_token.type == T_POW:
                self.node.insert(self.current_token)
                self.node.insert(fac1)
                self.advanceTk()
                if self.current_token.type not in (T_LPARAN, T_INT, T_FLOAT):
                    Error("Invalid power", "A power operator must be followed by '(' or 'integer'",
                          self.current_token.pos).raiseError()
                fac2 = self.parseFactor()
                self.node.insert(fac2)
                #fac1 = f"({fac1} ** {fac2})"
        return fac1


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


def run(text):
    lexer = Lexer(text)
    tokens = lexer.make_tokens()
    return tokens
