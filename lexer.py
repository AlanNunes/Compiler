from constant import *


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
    #parser = Parser(tokens)
    return tokens
