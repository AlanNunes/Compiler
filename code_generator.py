from constant import *
from ast import *

class ICodeGenerator:
    # ir: intermediate code
    def __init__(self, ir, symb_tbl):
        self.__ir = ir
        self.output = ""
        self.current_symb_tbl = symb_tbl

    def gen_else(self, node):
        pass

    def gen_else_if(self, node):
        pass

    def gen_if(self, node):
        pass

    def gen_var_declaration(self, node):
        pass

    def gen_var_assign(self, node):
        pass

    def gen_expr(self, node):
        pass

    def gen_type(self, token):
        pass

    def gen_op(self, token):
        pass

# TODO: Code generation for C# target machine language
class CSharp(ICodeGenerator):
    def __init__(self, ir, symb_tbl):
        super().__init__(ir, symb_tbl)

    def gen_stmt(self, node):
        pass

    def gen_else(self, node):
        body = ""
        return f"else\n{{{body}}}"

    def gen_else_if(self, node, output):
        cond = self.gen_expr(node.cond, "")
        body = ""
        option = ""
        if isinstance(node.option, If):
            option = self.gen_else_if(node.option, "")
        elif isinstance(node.option, Else):
            option = self.gen_else(node.option)
        output += f"else if ({cond})\n{{{body}}}\n{option}"
        return output

    def gen_if(self, node):
        cond = self.gen_expr(node.cond, "")
        body = ""
        option = ""
        if isinstance(node.option, If):
            option = self.gen_else_if(node.option, "")
        elif isinstance(node.option, Else):
            option = self.gen_else(node.option)
        return f"if ({cond})\n{{{body}}}\n{option}"

    # node: VarDeclare 
    def gen_var_declaration(self, node):
        id = node.node.left.token.value
        type = self.current_symb_tbl.getEntry(id)['type']
        typed_dec = self.gen_typed_declaration(id, type)
        res = self.gen_expr(node.node.right, "")
        return f"{typed_dec} = {res};"

    # node: Assign
    def gen_var_assign(self, node):
        id = node.node.left.token.value
        res = self.gen_expr(node.node.right, "")
        return f"{id} = {res};"

    def gen_expr(self, node, output):
        if isinstance(node, BinOp):
            op = self.gen_op(node.op)
            # TODO: Visit the left node
            left_res = self.gen_expr(node.left, output)
            # TODO: Visit the right node
            right_res = self.gen_expr(node.right, output)
            output += f"({left_res} {op} {right_res})"
            return output
        elif isinstance(node, Num):
            output += f"{node.value}"
            return output
        elif isinstance(node, Var):
            output += f"{node.token.value}"
            return output

    def gen_op(self, token):
        if token.type == T_PLUS:
            return "+"
        elif token.type == T_MINUS:
            return "-"
        elif token.type == T_MUL:
            return "*"
        elif token.type == T_DIV:
            return "/"
        elif token.type == T_GT:
            return ">"
        elif token.type == T_LT:
            return "<"
        elif token.type == T_GTEQ:
            return ">="
        elif token.type == T_LTEQ:
            return "<="
        elif token.type == T_EQUALITY:
            return "=="

    def gen_typed_declaration(self, id, type):
        if type == T_INT:
            return self.gen_integer_declaration(id)
        elif type == T_FLOAT:
            return self.gen_floating_declaration(id)
        elif type == T_STRING:
            return self.gen_string_declaration(id)
        # TODO: elif token.type == T_COLLECTION:

    def gen_integer_declaration(self, id):
        return f"int {id}"

    def gen_floating_declaration(self, id):
        return f"float {id}"

    def gen_string_declaration(self, id):
        return f"string {id}"

    #def gen_collection_declaration(self, id):
    #    return f"??? {id}"

    #def gen_type(self, token):
    #    if token.type == T_INT:
    #        return "int"
    #    elif token.type == T_FLOAT:
    #        return "float"
    #    elif token.type == T_STRING:
    #        return "string"
    #    # TODO: elif token.type == T_COLLECTION: