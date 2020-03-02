from constant import *
from error import *
from ast import *
import symbolTable

class NodeVisitor(object):
    def visit(self, node):
        if isinstance(node, BinOp):
            return self.visit_BinOp(node)
        elif isinstance(node, Num):
            return self.visit_Num(node)
        elif isinstance(node, Assign) or isinstance(node, VarDeclare):
            return self.visit_assign(node)


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.symb_table = symbolTable.SymbolTable()

    def visit_BinOp(self, node):
        if node.op.type == T_PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == T_MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == T_MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == T_DIV:
            return self.visit(node.left) / self.visit(node.right)
        elif node.op.type == T_POW:
            return self.visit(node.left) ** self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_assign(self, node):
        isDeclare = False
        if isinstance(node, VarDeclare):
            node = node.node
            isDeclare = True
        left = node.left.token
        right = self.visit(node.right)
        if isinstance(right, float) and not (right).is_integer():
            type = T_FLOAT
        else:
            type = T_INT
            right = int(right)
        if isDeclare:
            self.symb_table.insert(left.value, type, right, node.left.token.pos)
        return right



class Var(AST):
    def __init__(self, token):
        self.token = token

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class VarDeclare(AST):
    def __init__(self, node):
        self.node = node


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        self.ast = AST()

    def parse(self):
        if len(self.tokens) > 0:
            return self.parseStatement()
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
            t = self.parseExpr()
            self.advance()
            return t
        elif self.current_token.type in (T_KEYWORD, T_IDENTIFIER):
            node = self.variable()
            return node
        elif self.current_token.type == T_EQ:
            self.advance()
            return self.parseExpr()
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
        if self.current_token.type == T_EQ:
            self.parseExpr()
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

    def parseStatement(self):
        if self.current_token.type in (T_KEYWORD, T_IDENTIFIER):
            return self.parseAssignment()
        else:
            return self.parseExpr()

    def parseAssignment(self):
        isDeclare = False
        if self.current_token.type == T_KEYWORD:
            isDeclare = True
            self.advance()
        left = self.variable()
        # consume T_EQ token
        token = self.current_token
        right = self.parseExpr()
        assignNode = Assign(left=left, op=token, right=right)
        if isDeclare:
            node = VarDeclare(assignNode)
            return node
        return assignNode

    def variable(self):
        node = Var(self.current_token)
        self.advance()
        return node