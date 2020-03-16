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
        elif isinstance(node, Var):
            return self.visit_var(node)
        elif isinstance(node, String):
            return self.visit_String(node)


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.symb_table = symbolTable.SymbolTable()

    def visit_BinOp(self, node):
        if node.op.type == T_PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == T_MINUS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(left, str) and isinstance(right, str):
                return left.replace(right, "")
            return str(left - right)
        elif node.op.type == T_MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == T_DIV:
            right = self.visit(node.right)
            if right == 0: DividedByZeroError(node.right.token.pos).raiseError()
            return self.visit(node.left) / right
        elif node.op.type == T_POW:
            return self.visit(node.left) ** self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def visit_String(self, node):
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
        elif isDeclare and not right and right != 0:
            type = T_NOT_INITIALIZED
            right = None
        elif isinstance(right, str):
            type = T_STRING
        else:
            type = T_INT
            right = int(right)
        if isDeclare:
            self.symb_table.insert(left.value, type, right, node.left.token.pos)
        else:
            self.symb_table.update(left.value, type, right, node.left.token.pos)
        return right

    def visit_var(self, node):
        return self.symb_table.getValue(node.token)

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

class NotInitialized:
    def __init__(self, node):
        self.node = node


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()

    def parse(self):
        if len(self.tokens) > 0:
            return self.parseStatement()
        #Error("Empty code", "You can't run empty code", self.current_token.pos).raiseError()

    def advance(self):
        self.tok_idx += 1
        if self.tok_idx < len(self.tokens):
            self.current_token = self.tokens[self.tok_idx]
            return self.current_token
        return

    def getNextToken(self):
        return self.tokens[self.tok_idx + 1] if self.tok_idx + 1 < len(self.tokens) else None

    def parseFactor(self):
        if self.current_token.type in (T_INT, T_FLOAT):
            t = self.current_token
            number = Num(t)
            self.advance()
            if self.current_token.type in operators:
                nTok = self.getNextToken()
                if nTok != None and nTok.type not in operands + (T_LPARAN, T_IDENTIFIER):
                    SyntaxError(self.current_token.pos,
                                f"Expected a '(, identifier' but found {self.current_token}").raiseError()
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
        elif self.current_token.type in (T_DECLARE, T_IDENTIFIER):
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
                if self.current_token.type not in (T_LPARAN, T_INT, T_FLOAT, T_IDENTIFIER):
                    Error("Invalid power", "A power operator must be followed by '(' or 'integer'",
                          self.current_token.pos).raiseError()
            fac1 = BinOp(left=fac1, op=token, right=self.parseFactor())
        return fac1

    def parseStatement(self):
        if self.current_token.type == T_DECLARE:
            return self.parseAssignment()
        elif self.current_token.type == T_IDENTIFIER and self.getNextToken() and self.getNextToken().type == T_EQ:
            return self.parseAssignment()
        elif self.current_token.type == T_IF:
            return self.parseIfStatement()
        return self.parseExpr()


    def parseIfStatement(self):
        self.advance()
        # To do: build a condition structure
        # To do: build a body structure
        # To do: build a option (else/else if) structure

    def parseAssignment(self):
        isDeclare = False
        if self.current_token.type == T_DECLARE:
            isDeclare = True
            self.advance()
        left = self.variable()
        # consume T_EQ token
        token = self.current_token
        if token.type == T_IDENTIFIER and not self.getNextToken():
            assignNode = Assign(left=left, op=token, right=None)
        else:
            if self.getNextToken() and self.getNextToken().type == T_STRING:
                self.advance()
                right = String(self.current_token)
            else:
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