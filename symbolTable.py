from error import SymbolNotUinique


class SymbolTable():
    # tbl = [IDENTIFIER, TYPE, VALUE]
    def __init__(self, tbl=[]):
        self.tbl = tbl

    def insert(self, id, type, val, pos):
        if self.lookup(id):
            SymbolNotUinique(pos).raiseError()
        self.tbl.append([id, type, val])

    def lookup(self, id):
        return self.tbl[id]

    def print(self):
        for t in self.tbl:
            print(t)
