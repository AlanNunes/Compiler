class Error:
    def __init__(self, name, detail, pos):
        self.name = name
        self.detail = detail
        self.pos = pos

    def raiseError(self):
        print(f"'{self.name}': error ocurred in line {self.pos.ln+1}, col {self.pos.col}: {self.detail}")
        #raise SystemExit()


class DividedByZeroError(Error):
    def __init__(self, pos, name="DividedByZero", detail="You cannot divide a value by zero"):
        self.name = name
        self.detail = detail
        self.pos = pos


class SyntaxError(Error):
    def __init__(self, pos, detail, name="SyntaxError"):
        self.name = name
        self.detail = detail
        self.pos = pos


class NotUniqueSymbol(Error):
    def __init__(self, pos, detail="Identifier is already declared", name="SymbolNotUnique"):
        self.name = name
        self.detail = detail
        self.pos = pos

class NotFoundSymbol(Error):
    def __init__(self, pos, detail="You must declare this identifier before used it", name="NotFoundSymbol"):
        self.name = name
        self.detail = detail
        self.pos = pos


class TooManyArguments(Error):
    def __init__(self, pos, detail="Too much arguments specified", name="TooManyArguments"):
        self.name = name
        self.detail = detail
        self.pos = pos


class TooFewArguments(Error):
    def __init__(self, pos, detail="Too few arguments specified", name="TooFewArguments"):
        self.name = name
        self.detail = detail
        self.pos = pos


class RunTimeError(Error):
    def __init__(self, pos, detail, name="RunTimeError"):
        self.name = name
        self.detail = detail
        self.pos = pos