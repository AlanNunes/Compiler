from constant import *
from error import *


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def parse(self):
        if len(self.tokens) > 0:
            return self.parseExpr()
        Error("Empty code", "You can't run empty code", Position(0, 0, 0, "")).raiseError()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]
            return self.current_token
        return

    def getNextToken(self):
        return self.tokens[self.tok_idx+1] if len(self.tokens) > 0 else None

    def parseFactor(self):
        if self.current_token.type in (T_INT, T_FLOAT):
            t = self.current_token.value
            self.advance()
            if self.current_token.type in operators:
                nTok = self.getNextToken()
                if nTok != None and nTok.type not in operands + (T_LPARAN,):
                    SyntaxError(self.current_token.pos,
                                f"Expected a '+, -, /, *, ^, (' but found {self.current_token}").raiseError()
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
            SyntaxError(self.current_token.pos,
                        f"Expected a value or expression, but found '{self.current_token}'").raiseError()

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
                if self.current_token.type not in (T_LPARAN, T_INT, T_FLOAT):
                    Error("Invalid power", "A power operator must be followed by '(' or 'integer'",
                          self.current_token.pos).raiseError()
                fac2 = self.parseFactor()
                fac1 = fac1 ** fac2
        return fac1
