class AST(object):
    def __init__(self, token):
        self.token = token
        self.value = token.value


class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right


class Num(AST):
    pass


class String(AST):
    pass


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


class While(AST):
    def __init__(self, cond, body, option):
        self.cond = cond
        self.body = body
        self.option = option


class Loop(AST):
    def __init__(self, expr, body, variable=None, cond=None):
        self.variable = variable
        self.cond = cond
        self.expr = expr
        self.body = body

    #The types of "loop"
    #returns 0: loop expr COLON body ENDLOOP
    #returns 1: loop variable SEMICOLON expr COLON body ENDLOOP
    #returns 2: loop variable SEMICOLON cond SEMICOLON expr COLON body ENDLOOP
    def getType(self):
        if self.expr != None and self.variable == None and self.cond == None:
            return 0
        elif self.variable != None and self.cond == None:
            return 1
        else:
            return 2


class Print(AST):
    def __init__(self, val):
        self.val = val


class Collection(AST):
    def __init__(self, elements):
        self.elements = elements

    def add(self, e):
        self.elements.append(e)

    def isEmpty(self):
        return not self.elements

    def clear(self):
        self.elements = []


class Index:
    def __init__(self, v):
        self.v = v


class CollectionAccess:
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index


class CollectionAssign:
    def __init__(self, collAccess, val):
        self.collAccess = collAccess
        self.val = val


class Procedure:
    def __init__(self, identifier, args, body):
        self.identifier = identifier
        self.args = args
        self.body = body


# Represents a call to a procedure
class Activation:
    def __init__(self, id, args):
        self.id = id
        self.args = args


class Count:
    def __init__(self, obj):
        self.obj = obj


class Append:
    def __init__(self, collection, val):
        self.collection = collection
        self.val = val