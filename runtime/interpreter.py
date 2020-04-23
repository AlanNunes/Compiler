from constant import *
from error import *
from ast import *
from symbol_table import *
import uuid

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
        elif isinstance(node, Statement):
            return self.visit_statement(node)
        elif isinstance(node, If):
            return self.visit_if(node)
        elif isinstance(node, Else):
            return self.visit_else(node)
        elif isinstance(node, While):
            return self.visit_while(node)
        elif isinstance(node, Loop):
            return self.visit_loop(node)
        elif isinstance(node, Print):
            return self.visit_print(node)
        elif isinstance(node, Collection):
            return self.visit_collection(node)
        elif isinstance(node, Index):
            return self.visit_index(node)
        elif isinstance(node, CollectionAccess):
            return self.visit_collectionAccess(node)
        elif isinstance(node, Count):
            return self.visit_count(node)
        elif isinstance(node, Append):
            return self.visit_append(node)
        elif isinstance(node, CollectionAssign):
            return self.visist_collAssign(node)
        elif isinstance(node, Procedure):
            return self.visit_procedure(node)
        elif isinstance(node, Activation):
            return self.visit_activation(node)
        elif isinstance(node, Return):
            return self.visit_return(node)
        elif isinstance(node, MustReturn):
            return node
        else:
            return RuntimeError(pos=node.token.pos, detail=f"Didn't find an interpreter for {node}").raiseError()


class Interpreter(NodeVisitor):
    def __init__(self, parser):
        self.parser = parser
        self.current_symbTbl = SymbolTable("global")

    def visit_BinOp(self, node):
        if node.op.type == T_PLUS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(left, str) or isinstance(right, str):
                return str(self.visit(node.left)) + str(self.visit(node.right))
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == T_MINUS:
            left = self.visit(node.left)
            right = self.visit(node.right)
            if isinstance(left, str) and isinstance(right, str):
                return left.replace(right, "")
            return left - right
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
        elif isinstance(right, int):
            type = T_INT
            right = int(right)
        else:
            type = T_COLLECTION
            right = right
        if isDeclare:
            if not self.current_symbTbl.insert(id=left.value, type=type, val=right):
                return NotUniqueSymbol(pos=left.pos, detail=f"Identifier '{left.value}' is already declared").raiseError()
        else:
            if not self.current_symbTbl.update(id=left.value, type=type, val=right):
                return NotFoundSymbol(pos=left.pos, detail=f"Identifier '{left.value}' is not declared").raiseError()
        return right

    def visit_var(self, node):
        val, success = self.current_symbTbl.lookup(node.token.value)
        if success:
            return val
        return NotFoundSymbol(pos=node.token.pos).raiseError()

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

    def visit_statement(self, node):
        rtn = None
        for stmt in node.stmts:
            rtn = self.visit(stmt)
            if isinstance(rtn, MustReturn):
                return rtn
        return rtn

    def visit_if(self, node):
        current_parent = self.current_symbTbl
        cond = self.visit(node.cond)
        if cond == 1:
            self.current_symbTbl = SymbolTable(parent=current_parent)
            rtn = self.visit(node.body)
            self.current_symbTbl = current_parent
            return rtn
        if node.option == None:
            return
        if isinstance(node.option, If):
            return self.visit_if(node.option)
        elif isinstance(node.option, Else):
            rtn = self.visit(node.option)
            return rtn
        return

    def visit_while(self, node):
        current_parent = self.current_symbTbl
        self.current_symbTbl = SymbolTable(parent=current_parent)
        rtn = None
        while self.visit(node.cond) == 1:
            rtn = self.visit(node.body)
        self.current_symbTbl = current_parent
        return rtn

    def visit_loop(self, node):
        current_parent = self.current_symbTbl
        self.current_symbTbl = SymbolTable(parent=current_parent)
        rtn = None
        lType = node.getType()
        if lType == 0:
            count = self.visit(node.expr)
            i = 0
            while i != abs(count):
                rtn = self.visit(node.body)
                i += 1
        elif lType == 1:
            count = self.visit(node.expr)
            i = self.visit(node.variable)
            while i != count:
                rtn = self.visit(node.body)
                i += 1
                if isinstance(node.variable, VarDeclare):
                    var = node.variable.node
                    self.current_symbTbl.update(var.left.token.value, i)
                else:
                    var = node.variable if node.variable.token.type == T_IDENTIFIER else node.variable.left
                    self.current_symbTbl.update(var.token.value, i)
        else:
            var = node.variable.node
            self.current_symbTbl.insert(id=var.left.token.value, type=var.right.token.type, val=var.right.token.value)
            while self.visit(node.cond) == 1:
                rtn = self.visit(node.body)
                res = self.visit(node.expr)
                self.current_symbTbl.update(id=var.left.token.value, val=res)
        self.current_symbTbl = current_parent
        return rtn

    def visit_print(self, node):
        rtn = self.visit(node.val)
        print(rtn)
        return rtn

    def visit_else(self, node):
        current_parent = self.current_symbTbl
        self.current_symbTbl = SymbolTable(parent=current_parent)
        rtn = self.visit(node.body)
        self.current_symbTbl = current_parent
        return rtn


    def visit_collectionAccess(self, node):
        indexes = []
        value, success = self.current_symbTbl.lookup(node.identifier.value)
        if not success:
            return NotFoundSymbol(pos=node.identifier.pos)
        for i in node.index:
            indexes.append(self.visit(i))
        for i in indexes:
            v = value[i]
        return v

    def visit_index(self, node):
        return self.visit(node.v)

    def visit_collection(self, node):
        v = []
        for i in node.elements:
            v.append(self.visit(i))
        return v

    def visit_count(self, node):
        val = self.visit(node.obj)
        if not isinstance(val, list):
            return
        return len(val)

    def visit_append(self, node):
        identifier = node.collection.token
        value, success = self.current_symbTbl.lookup(identifier.value)
        if not success:
            return NotFoundSymbol(pos=identifier.pos)
        value.append(self.visit(node.val))
        self.current_symbTbl.update(identifier.value, value)
        return value

    def visist_collAssign(self, node):
        coll, success = self.current_symbTbl.lookup(node.collAccess.identifier.value)
        indexes = []
        value, success_ = self.current_symbTbl.lookup(node.collAccess.identifier.value)
        if not success or not success_:
            return NotFoundSymbol(pos=node.collAccess.identifier.pos)
        last = None
        for i in node.collAccess.index:
            indexes.append(self.visit(i))
        iLen = len(indexes)
        for i in range(iLen):
            idx = indexes[i]
            v = value[idx]
            if i + 1 == iLen:
                last = value[i]
            vArg = v
        last = value
        return teste

    def visit_procedure(self, node):
        id = node.identifier.value
        res = self.current_symbTbl.insert(id=id, type=T_FUNCTION, val=node)
        if not res:
            return RunTimeError(pos=node.identifier.pos, detail=f"The function '{id.value}' is already defined").raiseError()
        return

    def visit_activation(self, node):
        # Check if the activation exists
        fun, success = self.current_symbTbl.lookup(node.id.value)
        if not success:
            return RunTimeError(pos=node.id.pos, detail=f"The function '{node.id.value}' is not defined. You cannot call functions not defined").raiseError()
        parentST = self.current_symbTbl
        self.current_symbTbl = SymbolTable(parent=parentST)
        if len(fun.args) != len(node.args):
            return TooFewArguments(pos=node.id.pos).raiseError()
        for i in range(len(fun.args)):
            id = fun.args[i]
            val = node.args[i]
            assignNode = Assign(left=id, op=T_EQ, right=val)
            declare = VarDeclare(assignNode)
            self.visit(declare)
        for stmt in fun.body.stmts:
            if isinstance(stmt, Return):
                rtn = self.visit(stmt.val)
                return rtn
            rtn = self.visit(stmt)
            if isinstance(rtn, MustReturn):
                return self.visit(rtn.val)
        self.current_symbTbl = parentST
        return

    def visit_return(self, node):
        return MustReturn(node.val)