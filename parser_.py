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
        elif node.op.type in (T_GT, T_LT, T_GTEQ, T_LTEQ):
            return self.visit_arith_expr(node)
        elif node.op.type in (T_AND, T_OR, T_EQUALITY):
            return self.visist_comp_expr(node)

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

    def visit_arith_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        t = node.op.type
        if t == T_GT:
            return 1 if (left > right) else 0
        elif t == T_LT:
            return 1 if (left < right) else 0
        elif t == T_GTEQ:
            return 1 if (left >= right) else 0
        elif t == T_LTEQ:
            return 1 if (left <= right) else 0

    def visist_comp_expr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        # if the values are not empty strings, convert it to 1
        if isinstance(left, str) and not str(left):
            left = 0
        if isinstance(right, str) and not str(right):
            right = 0
        t = node.op.type
        if t == T_AND:
            return 1 if (left != 0 and right != 0) else 0
        elif t == T_OR:
            return 1 if (left != 0 or right != 0) else 0
        elif t == T_EQUALITY:
            return 1 if (left == right) else 0

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
        stmts = Statement([])
        if len(self.tokens) > 0:
            while self.current_token.type != T_EOF:
                stmt = self.parseStatement()
                if stmt != None:
                    stmts.add(stmt)
        return stmts
        #Error("Empty code", "You can't run empty code",
        #self.current_token.pos).raiseError()

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
            if self.current_token.type in operators + (T_GT, T_LT, T_GTEQ, T_LTEQ):
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
        elif self.current_token.type == T_STRING:
            t = String(self.current_token)
            self.advance()
            return t
        else:
            SyntaxError(self.current_token.pos,
                        f"Expected a value or expression, but found '{self.current_token}'").raiseError()

    def parseExpr(self):
        fac1 = self.parseTerm()
        while self.current_token.type in [T_PLUS, T_MINUS, T_AND, T_OR, T_EQUALITY]:
            token = self.current_token
            #if self.current_token.type == T_PLUS:
            #    self.advance()
            #elif self.current_token.type == T_MINUS:
            #    self.advance()
            self.advance()
            fac1 = BinOp(left=fac1, op=token, right=self.parseTerm())
        if self.current_token.type == T_EQ:
            self.parseExpr()
        return fac1

    def parseTerm(self):
        fac1 = self.parseFactor()
        while self.current_token.type in [T_MUL, T_DIV, T_POW, T_GT, T_LT, T_GTEQ, T_LTEQ]:
            token = self.current_token
            self.advance()
            fac1 = BinOp(left=fac1, op=token, right=self.parseFactor())
        return fac1

    def parseStatement(self):
        if self.current_token.type == T_DECLARE:
            return self.parseAssignment()
        elif self.current_token.type == T_IDENTIFIER and self.getNextToken() and self.getNextToken().type == T_EQ:
            return self.parseAssignment()
        elif self.current_token.type == T_IF:
            return self.parseIf()
        return self.parseExpr()


    def parseIf(self):
        self.advance()
        cond = self.parseExpr()
        if not self.current_token.type == T_COLON:
            SyntaxError(pos=self.current_token.pos, detail=f"Expected a ':' but found {self.current_token}").raiseError()
        self.advance()
        t = self.current_token
        stmt = Statement([])
        while self.current_token.type not in (T_ENDIF, T_ELSEIF, T_EOF):
            stmt.add(self.parseStatement())
        body = stmt
        option = None
        if self.current_token.type == T_ENDIF:
            self.advance()
        elif self.current_token.type == T_ELSEIF:
            option = self.parseIf()
        return If(cond=cond, body=body, option=option)
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