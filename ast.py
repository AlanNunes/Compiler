class AST(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Statement(AST):
    def __init__(self, stmts):
        self.stmts = stmts

    def add(self, stmt):
        self.stmts.append(stmt)


class If(AST):
    def __init__(self, cond, body, option):
        self.cond = cond
        self.body = body
        self.option = option

class ElseIf(If):
    pass

class Else(AST):
    def __init__(self, body):
        self.body = body

class Condition(AST):
    def __init__(self, expr):
        self.expr = expr

class Num(AST):
    pass


class String(AST):
    pass