from constant import *
from error import *
from ast import *
from symbol_table import *
from interpreter import Interpreter, NodeVisitor


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tok_idx = -1
        self.advance()
        self.current_symb_tbl = SymbolTable("global")
        self.error = False

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
            if self.getNextToken() and self.getNextToken().type == T_LPARAN:
                node = self.parseActivation()
                return node
            node = self.variable()
            return node
        elif self.current_token.type == T_EQ:
            self.advance()
            return self.parseExpr()
        elif self.current_token.type == T_STRING:
            t = String(self.current_token)
            self.advance()
            return t
        elif self.current_token.type == T_COUNT:
            return self.parseBuiltInProcedures()
        else:
            self.error = True
            SyntaxError(self.current_token.pos,
                        f"Expected a value or expression, but found '{self.current_token}'").raiseError()
            self.advance()

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
        elif self.current_token.type == T_WHILE:
            return self.parseWhile()
        elif self.current_token.type == T_LOOP:
            return self.parseLoop()
        elif self.current_token.type == T_PRINT:
            return self.parsePrint()
        elif self.current_token.type == T_COMMA:
            self.advance()
        elif self.current_token.type == T_IDENTIFIER and self.getNextToken() and self.getNextToken().type == T_L_BRACKET:
            return self.parseCollectionAccess()
        elif self.current_token.type in builtInProc:
            return self.parseBuiltInProcedures()
        elif self.current_token.type == T_FUNCTION:
            return self.parseFunction()
        elif self.current_token.type == T_IDENTIFIER and self.getNextToken() and self.getNextToken().type == T_LPARAN:
            return self.parseActivation()
        elif self.current_token.type == T_RETURN:
            return self.parseReturn()
        return self.parseExpr()


    def parsePrint(self):
        self.advance()
        return Print(val=self.parseStatement())

    def parseLoop(self):
        self.advance()
        # Create symbol table for while and set it as current
        parentSymbTbl = self.current_symb_tbl
        loop_symbTbl = SymbolTable(parent=parentSymbTbl)
        self.current_symb_tbl = loop_symbTbl
        # Finish symbol table creation
        var = None
        expr = None
        stmt = self.parseStatement()
        if isinstance(stmt, Var) or isinstance(stmt, Assign) or isinstance(stmt, VarDeclare):
            var = stmt
            if self.current_token.type != T_SEMICOLON:
                SyntaxError(pos=self.current_token.pos, detail=f"Expected a ';' but found {self.current_token}").raiseError()
            self.advance()
            stmt = self.parseStatement()
            if isinstance(stmt, BinOp) or isinstance(stmt, Num) or isinstance(stmt, Assign):
                if not isinstance(stmt, Num) and stmt.op.type in (T_LT, T_LTEQ, T_GT, T_GTEQ, T_EQUALITY):
                    cond = stmt
                    if self.current_token.type != T_SEMICOLON:
                        SyntaxError(pos=self.current_token.pos, detail=f"Expected a ';' but found {self.current_token}").raiseError()
                    self.advance()
                    expr = self.parseStatement()
                    if self.current_token.type != T_COLON:
                        SyntaxError(pos=self.current_token.pos, detail=f"Expected a ':' but found {self.current_token}").raiseError()
                    self.advance()
                    stmt = Statement([])
                    while self.current_token.type not in (T_ENDLOOP, T_EOF):
                        stmt.add(self.parseStatement())
                    body = stmt
                    self.advance()
                    # Put back the parent symbol table as current
                    self.current_symb_tbl = parentSymbTbl
                    return Loop(variable=var, cond=cond, expr=expr, body=body, symb_tbl=loop_symbTbl)
                expr = stmt
                if self.current_token.type != T_COLON:
                    SyntaxError(pos=self.current_token.pos, detail=f"Expected a ':' but found {self.current_token}").raiseError()
                self.advance()
                stmt = Statement([])
                while self.current_token.type not in (T_ENDLOOP, T_EOF):
                    stmt.add(self.parseStatement())
                body = stmt
                self.advance()
                # Put back the parent symbol table as current
                self.current_symb_tbl = parentSymbTbl
                return Loop(variable=var, expr=expr, body=body, symb_tbl=loop_symbTbl)
        elif isinstance(stmt, BinOp) or isinstance(stmt, Num):
            expr = stmt
            if self.current_token.type != T_COLON:
                SyntaxError(pos=self.current_token.pos, detail=f"Expected a ':' but found {self.current_token}").raiseError()
            self.advance()
            stmt = Statement([])
            while self.current_token.type not in (T_ENDLOOP, T_EOF):
                stmt.add(self.parseStatement())
            body = stmt
            self.advance()
            # Put back the parent symbol table as current
            self.current_symb_tbl = parentSymbTbl
            return Loop(expr=expr, body=body, symb_tbl=loop_symbTbl)
        else:
            SyntaxError(pos=self.current_token.pos, detail=f"Expected an expression or variable, but found '{self.current_token}'").raiseError()


    def parseWhile(self):
        self.advance()
        cond = self.parseExpr()
        if not self.current_token.type == T_COLON:
            self.error = True
            SyntaxError(pos=self.current_token.pos, detail=f"Expected a ':' but found {self.current_token}").raiseError()
        self.advance()
        stmt = Statement([])
        # Create symbol table for while and set it as current
        parentSymbTbl = self.current_symb_tbl
        while_symbTbl = SymbolTable(parent=parentSymbTbl)
        self.current_symb_tbl = while_symbTbl
        # Finish symbol table creation
        while self.current_token.type not in (T_ENDWHILE, T_EOF):
            stmt.add(self.parseStatement())
        body = stmt
        if self.current_token.type != T_ENDWHILE:
            self.error = True
            return SyntaxError(pos=self.current_token.pos, detail=f"Expected a 'endwhile' but found '{self.current_token}'").raiseError()
        self.advance()
        # Put back the parent symbol table as current
        self.current_symb_tbl = parentSymbTbl
        return While(cond=cond, body=body, symb_tbl=while_symbTbl)

    def parseIf(self):
        self.advance()
        cond = self.parseExpr()
        if not self.current_token.type == T_COLON:
            self.error = True
            return SyntaxError(pos=self.current_token.pos, detail=f"Expected a ':' but found {self.current_token}").raiseError()
        self.advance()
        t = self.current_token
        stmt = Statement([])
        # Create symbol table for while and set it as current
        parentSymbTbl = self.current_symb_tbl
        if_symbTbl = SymbolTable(parent=parentSymbTbl)
        self.current_symb_tbl = if_symbTbl
        # Finish symbol table creation
        while self.current_token.type not in (T_ENDIF, T_ELSEIF, T_ELSE, T_ENDWHILE, T_ENDLOOP, T_EOF):
            stmt.add(self.parseStatement())
        body = stmt
        option = None
        # Put back the parent symbol table as current
        self.current_symb_tbl = parentSymbTbl
        if self.current_token.type == T_ENDIF:
            self.advance()
        elif self.current_token.type == T_ELSEIF:
            option = self.parseIf()
        elif self.current_token.type == T_ELSE:
            option = self.parseElse()
        else:
            self.error = True
            return SyntaxError(pos=self.current_token.pos, detail=f"Expected a 'endif', 'elseif', 'else' but found {self.current_token}").raiseError()
        return If(cond=cond, body=body, option=option, symb_tbl=if_symbTbl)

    def parseElse(self):
        self.advance()
        if not self.current_token.type == T_COLON:
            return SyntaxError(pos=self.current_token.pos, detail=f"Expected a ':' but found {self.current_token}").raiseError()
        self.advance()
        stmt = Statement([])
        # Create symbol table for while and set it as current
        parentSymbTbl = self.current_symb_tbl
        else_symbTbl = SymbolTable(parent=parentSymbTbl)
        self.current_symb_tbl = else_symbTbl
        # Finish symbol table creation
        while self.current_token.type not in (T_ENDIF, T_EOF):
            stmt.add(self.parseStatement())
        body = stmt
        if self.current_token.type != T_ENDIF:
            self.error = True
            return SyntaxError(pos=self.current_token.pos, detail=f"Expected a 'endif' but found {self.current_token}").raiseError()
        self.advance()
        # Put back the parent symbol table as current
        self.current_symb_tbl = parentSymbTbl
        return Else(body, symb_tbl=else_symbTbl)

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
            if self.getNextToken().type == T_STRING:
                self.advance()
                right = String(self.current_token)
                self.advance()
            elif self.getNextToken().type == T_L_BRACKET:
                self.advance()
                self.advance()
                right = self.parseCollection()
            else:
                right = self.parseExpr()
            assignNode = Assign(left=left, op=token, right=right)
        type = self.getVarType(assignNode.right, self.current_symb_tbl)
        if isDeclare:
            res = self.current_symb_tbl.insert(id=left.token.value, type=type, val=assignNode.right)
            if not res:
                self.error = True
                return NotUniqueSymbol(pos=left.token.pos).raiseError()
            node = VarDeclare(assignNode)
            return node
        #res = self.current_symb_tbl.update(id=left.token.value, val=assignNode.right, type=type)
        #if not res:
        #    NotFoundSymbol(pos=left.token.pos).raiseError()
        #    self.error = True
        return assignNode

    def variable(self):
        # TODO: Check if the var exists in the symbol table, if else thorw a compiler error
        if not self.current_symb_tbl.lookup(self.current_token.value):
            self.error = True
            return NotFoundSymbol(pos=self.current_token.pos).raiseError()
        node = Var(self.current_token)
        self.advance()
        return node

    def parseCollection(self):
        collection = Collection([])
        while self.current_token.type != T_R_BRACKET:
            if self.current_token.type == T_COMMA:
                self.advance()
            if self.current_token.type == T_L_BRACKET:
                self.advance()
                res = self.parseCollection()
            else:
                res = self.parseStatement()
            collection.add(res)
        self.advance()
        return collection

    def parseCollectionAccess(self):
        identifier = self.current_token
        self.advance()
        indexes = []
        while self.current_token.type == T_L_BRACKET:
            self.advance()
            index = Index(self.parseExpr())
            indexes.append(index)
            self.advance()
        collectionAccess = CollectionAccess(identifier, indexes)
        if self.current_token.type == T_EQ:
            self.advance()
            right = self.parseExpr()
            return CollectionAssign(collAccess=collectionAccess, val=right)
        return collectionAccess

    def parseBuiltInProcedures(self):
        if self.current_token.type == T_COUNT:
            self.advance()
            if self.current_token.type != T_LPARAN:
                return SyntaxError(pos=self.current_token.pos, detail=f"Expected a '(' but found {self.current_token}").raiseError()
            self.advance()
            args = self.getArgs()
            if self.current_token.type != T_RPARAN:
                return SyntaxError(pos=self.current_token.pos, detail=f"Expected a ')' but found {self.current_token}").raiseError()
            self.advance()
            if len(args) > 1:
                return TooManyArguments(pos=self.current_token.pos, detail=f"Too much arguments specified at procedure. 'Count' expected only 1 argument").raiseError()
            return Count(args[0])
        if self.current_token.type == T_APPEND:
            self.advance()
            if self.current_token.type != T_LPARAN:
                return SyntaxError(pos=self.current_token.pos, detail=f"Expected a '(' but found {self.current_token}").raiseError()
            self.advance()
            args = self.getArgs()
            if self.current_token.type != T_RPARAN:
                return SyntaxError(pos=self.current_token.pos, detail=f"Expected a ')' but found {self.current_token}").raiseError()
            self.advance()
            if len(args) < 2:
                return TooFewArguments(pos=self.current_token.pos, detail=f"Too few arguments specified at procedure. 'Append' expected 2 arguments").raiseError()
            elif len(args) > 2:
                return TooManyArguments(pos=self.current_token.pos, detail=f"Too much arguments specified at procedure. 'Append' expected 2 arguments").raiseError()
            return Append(args[0], args[1])

    def parseFunction(self):
        self.advance()
        if self.current_token.type != T_IDENTIFIER:
            # TODO: Throw an exception
            return
        id = self.current_token
        self.advance()
        if self.current_token.type != T_LPARAN:
            # TODO: Throw an exception
            return
        self.advance()
        args = self.getArgs()
        for v in args:
            if v.token.type != T_IDENTIFIER:
                return SyntaxError(pos=self.current_token.pos, detail=f"You can only use identifier in arguments of a function").raiseError()
        if self.current_token.type != T_RPARAN:
            # TODO: Throw an exception
            return
        self.advance()
        if self.current_token.type != T_COLON:
            # TODO: Throw an exception
            return
        self.advance()
        stmts = Statement([])
        isVoid = True
        while self.current_token.type != T_ENDFUN:
            if self.current_token.type == T_RETURN:
                isVoid = False
            stmts.add(self.parseStatement())
        self.advance()
        return Procedure(identifier=id, args=args, body=stmts, isVoid=isVoid)

    def parseActivation(self):
        id = self.current_token
        self.advance()
        if self.current_token.type != T_LPARAN:
            # TODO: Throw an exception
            return
        self.advance()
        args = self.getArgs()
        if self.current_token.type != T_RPARAN:
            # TODO: Throw an exception
            return
        self.advance()
        symb_tbl = SymbolTable(parent=self.current_symb_tbl)
        return Activation(id=id, args=args, symb_tbl=symb_tbl)

    def parseReturn(self):
        self.advance()
        rtn = self.parseExpr()
        return Return(rtn)

    def getArgs(self):
        args = []
        while self.current_token.type != T_RPARAN:
            args.append(self.parseExpr())
            if self.current_token.type == T_COMMA:
                self.advance()
        return args

    def getVarType(self, node, symb_tbl):
        val = Interpreter(NodeVisitor, symb_tbl).visit(node)
        if isinstance(val, int):
            return T_INT
        elif isinstance(val, float):
            return T_FLOAT
        elif isinstance(val, str):
            return T_STRING
        elif isinstance(val, list):
            return T_COLLECTION
        elif val == None:
            return T_NOT_INITIALIZED
        else:
            # TODO: compiler error
            return