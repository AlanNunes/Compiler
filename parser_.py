from constant import *
from error import *
from ast import *

class NodeVisitor(object):
    def visit(self, node):
        if isinstance(node, BinOp):
            return self.visit_BinOp(node)
        elif isinstance(node, Num):
            return self.visit_Num(node)


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser

    def visit_BinOp(self, node):
        if node.op.type == T_PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == T_MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == T_MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == T_DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        self.ast = AST()

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
            t = self.current_token
            number = Num(t)
            self.advance()
            if self.current_token.type in operators:
                nTok = self.getNextToken()
                if nTok != None and nTok.type not in operands + (T_LPARAN,):
                    SyntaxError(self.current_token.pos,
                                f"Expected a '+, -, /, *, ^, (' but found {self.current_token}").raiseError()
            return number
        elif self.current_token.type == T_LPARAN:
            self.advance()
            t = self.parseExpr()
            self.advance()
            return t
        elif self.current_token.type == T_POW:
            self.advance()
            t = self.parsePow()
            self.advance()
            return t
        elif self.current_token.type in (T_KEYWORD, T_IDENTIFIER, T_EQ):
            self.advance()
            t = self.parseExpr()
            self.advance()
            return t
        else:
            SyntaxError(self.current_token.pos,
                        f"Expected a value or expression, but found '{self.current_token}'").raiseError()

    def parseExpr(self):
        fac1 = self.parseTerm()
        while self.current_token.type == T_PLUS or self.current_token.type == T_MINUS:
            token = self.current_token
            if self.current_token.type == T_PLUS:
                self.advance()
            elif self.current_token.type == T_MINUS:
                self.advance()
            fac1 = BinOp(left=fac1, op=token, right=self.parseTerm())
        while self.current_token.type == T_KEYWORD:
            token = self.current_token
            self.advance()
            if self.current_token.type != T_IDENTIFIER:
                SyntaxError(
                    pos=self.pos, detail=f"Expected a identifier, but found '{self.current_token}'")
            self.advance()
            if self.current_token.type != T_EQ:
                SyntaxError(
                    pos=self.pos, detail=f"Expected a identifier, but found '{self.current_token}'")
            self.advance()
        return fac1

    def parseTerm(self):
        fac1 = self.parseFactor()
        while self.current_token.type == T_MUL or self.current_token.type == T_DIV or self.current_token.type == T_POW:
            token = self.current_token
            if self.current_token.type == T_MUL:
                self.advance()
            elif self.current_token.type == T_DIV:
                self.advance()
            elif self.current_token.type == T_POW:
                self.advance()
                if self.current_token.type not in (T_LPARAN, T_INT, T_FLOAT):
                    Error("Invalid power", "A power operator must be followed by '(' or 'integer'",
                          self.current_token.pos).raiseError()
            fac1 = BinOp(left=fac1, op=token, right=self.parseFactor())
        return fac1
