from constant import *

class AST:
    def __init__(self, nodes, symb_tbl=None):
        self.nodes = nodes
        self.symb_tbl = symb_tbl

    def print(self):
        print("="*80)
        print("="*22 + "   Printing Abstract Syntax Tree   " + "="*23)
        print("="*80)
        print("\n")
        self.print_tree(self.nodes, 0)

    def print_tree(self, node, level, prefix_name=""):
        if not isinstance(node, BinOp) and not isinstance(node, Assign):
            prefix = "      |" if level > 0 else ""
            for i in range(level):
                if i != level - 1:
                    prefix +="______|"
            if isinstance(node, int) or isinstance(node, float) or isinstance(node, str):
                val = f"->{prefix_name} {node}" if not isinstance(node, str) else f"->{prefix_name} '{node}'"
                print(prefix + val)
                return
            val = f"->{prefix_name} {node}"
            print(prefix + val)
        else:
            level -= 1
        if isinstance(node, Statement):
            for child in node.stmts:
                self.print_tree(child, level + 1)
        elif isinstance(node, BinOp):
            self.print_tree(node.left, level + 2)
            self.print_tree(node.op, level + 1)
            self.print_tree(node.right, level + 2)
        elif isinstance(node, Num):
            self.print_tree(node.value, level + 1)
        elif isinstance(node, String):
            self.print_tree(node.value, level + 1)
        elif isinstance(node, If):
            self.print_tree(node.cond, level)
            self.print_tree(node.body, level)
            if node.option:
                self.print_tree(node.option, level + 1)
        elif isinstance(node, Else):
            self.print_tree(node.body, level + 1)
        elif isinstance(node, While):
            self.print_tree(node.cond, level)
            self.print_tree(node.body, level)
        elif isinstance(node, Condition):
            self.print_tree(node.expr, level + 1)
        elif isinstance(node, VarDeclare):
            self.print_tree(node.node.left, level + 2)
            self.print_tree(node.node.op, level + 1)
            self.print_tree(node.node.right, level + 2)
        elif isinstance(node, Assign):
            self.print_tree(node.left, level + 2)
            self.print_tree(node.op, level + 1)
            self.print_tree(node.right, level + 2)
        elif isinstance(node, Loop):
            if node.variable:
                self.print_tree(node.variable, level)
            if node.cond:
                self.print_tree(node.cond.left, level + 1)
                self.print_tree(node.cond.op, level)
                self.print_tree(node.cond.right, level + 1)
            self.print_tree(node.expr.left, level + 1)
            self.print_tree(node.expr.op, level)
            self.print_tree(node.expr.right, level + 1)
            self.print_tree(node.body, level)
        elif isinstance(node, Procedure):
            self.print_tree(node.identifier, level + 1, " Id:")
            for child in node.args:
                self.print_tree(child, level + 1, " Arg:")
            self.print_tree(node.body, level + 1)
        elif isinstance(node, Return):
            self.print_tree(node.val, level + 1)
        elif isinstance(node, Activation):
            self.print_tree(node.id, level + 1, " Id:")
            for child in node.args:
                self.print_tree(child, level + 1, " Arg:")
        elif isinstance(node, Token):
            if node.value:
                self.print_tree(node.value, level + 1)
        elif isinstance(node, Print):
            self.print_tree(node.val, level + 1)
        elif isinstance(node, Var):
            if not self.symb_tbl:
                return
            res = self.symb_tbl.lookup(node.token.value)
            if res[1]:
                self.print_tree(res[0], level + 1)
            

class Token:
    def __init__(self, type_, pos, value=None):
        self.type = type_
        self.value = value
        self.pos = pos

    def __repr__(self):
        if self.value:
            return f'{self.value}'
        elif self.type == T_EQ:
            return "="
        elif self.type == T_GT:
            return ">"
        elif self.type == T_LT:
            return "<"
        elif self.type == T_GTEQ:
            return ">="
        elif self.type == T_LTEQ:
            return "<="
        elif self.type == T_EQUALITY:
            return "=="
        elif self.type == T_PLUS:
            return "+"
        elif self.type == T_MINUS:
            return "-"
        elif self.type == T_MUL:
            return "*"
        elif self.type == T_DIV:
            return "/"
        else:
            return self.__class__.__name__


class Node:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        if self.token:
            return f'{self.token.value}'
        return self.__class__.__name__


class BinOp(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def __repr__(self):
        if self.op:
            return f'{self.op}'
        return self.__class__.__name__


class Num(Node):
    def __repr__(self):
        return self.__class__.__name__


class String(Node):
    pass


class Statement(Node):
    def __init__(self, stmts):
        self.stmts = stmts

    def add(self, stmt):
        self.stmts.append(stmt)
    
    def __repr__(self):
        return "Statements"


class If(Node):
    def __init__(self, cond, body, option, symb_tbl):
        self.cond = cond
        self.body = body
        self.option = option
        self.symb_tbl = symb_tbl

    def __repr__(self):
        return "If"

class ElseIf(If):
    pass

class Else(Node):
    def __init__(self, body, symb_tbl):
        self.body = body
        self.symb_tbl = symb_tbl

    def __repr__(self):
        return "Else"

class Condition(Node):
    def __init__(self, expr):
        self.expr = expr

    def __repr__(self):
        return "Condition"


class While(Node):
    def __init__(self, cond, body, symb_tbl):
        self.cond = cond
        self.body = body
        self.symb_tbl = symb_tbl

    def __repr__(self):
        return "While"


class Loop(Node):
    def __init__(self, expr, body, symb_tbl, variable=None, cond=None):
        self.variable = variable
        self.cond = cond
        self.expr = expr
        self.body = body
        self.symb_tbl = symb_tbl

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

    def __repr__(self):
        return "Loop"


class Print(Node):
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "Print"


class Collection(Node):
    def __init__(self, elements):
        self.elements = elements

    def add(self, e):
        self.elements.append(e)

    def isEmpty(self):
        return not self.elements

    def clear(self):
        self.elements = []

    def __repr__(self):
        return "Collection"


class Index:
    def __init__(self, v):
        self.v = v

    def __repr__(self):
        return "Index"


class CollectionAccess:
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index

    def __repr__(self):
        return "CollectionAccess"


class CollectionAssign:
    def __init__(self, collAccess, val):
        self.collAccess = collAccess
        self.val = val

    def __repr__(self):
        return "CollectionAssign"


class Procedure:
    def __init__(self, identifier, args, body, isVoid=True):
        self.identifier = identifier
        self.args = args
        self.body = body
        self.isVoid = isVoid

    def __repr__(self):
        return self.__class__.__name__


# Represents a call to a procedure
class Activation:
    def __init__(self, id, args, symb_tbl):
        self.id = id
        self.args = args
        self.symb_tbl = symb_tbl

    def __repr__(self):
        return self.__class__.__name__


class Count:
    def __init__(self, obj):
        self.obj = obj

    def __repr__(self):
        return f"Count"


class Append:
    def __init__(self, collection, val):
        self.collection = collection
        self.val = val

    def __repr__(self):
        return f"Append ({self.collection})"


class Return:
    def __init__(self, val):
        self.val = val

    def __repr__(self):
        return "Return"


class Var(Node):
    def __init__(self, token):
        self.token = token

    def __repr__(self):
        return f"{self.token.value}"

class Assign(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def __repr__(self):
        return "="

class VarDeclare(Node):
    def __init__(self, node):
        self.node = node

    def __repr__(self):
        return "VarDeclare"

class NotInitialized:
    def __init__(self, node):
        self.node = node


class MustReturn:
    def __init__(self, val):
        self.val = val