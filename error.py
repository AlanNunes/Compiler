class Error:
    def __init__(self, name, detail, pos):
        self.name = name
        self.detail = detail
        self.pos = pos

    def raiseError(self):
        print(f"'{self.name}': error ocurred in line {self.pos.ln+1}, col {self.pos.col}: {self.detail}")
        raise SystemExit()


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


class SymbolNotUinique(Error):
    def __init__(self, pos, detail="You cannot declare to symbols", name="SymbolNotUnique"):
        self.name = name
        self.detail = detail
        self.pos = pos