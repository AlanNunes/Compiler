from error import NotUniqueSymbol, NotFoundSymbol


class SymbolTable():
    # tbl = [IDENTIFIER, TYPE, VALUE]
    def __init__(self, tbl={}):
        self.tbl = tbl

    def insert(self, id, type, val, pos):
        if self.lookup(id):
            NotUniqueSymbol(pos).raiseError()
            return
        self.tbl[id] = {"type": type, "value": val}

    def update(self, id, type, val, pos):
        if not self.lookup(id):
            NotFoundSymbol(pos).raiseError()
            return
        self.tbl[id] = {"type": type, "value": val}

    def lookup(self, id):
        return id in self.tbl

    def getValue(self, id):
        return self.tbl[id.value]["value"] if self.lookup(id.value) else NotFoundSymbol(id.pos).raiseError()

    def print(self):
        #print("############################################################################")
        #print("##                              Symbol Table                              ##")
        #print("############################################################################")
        print('#'*70)
        print('{:^70}'.format("Symbol Table"))
        print('\n')
        for t in self.tbl.items():
            print(f'{t}')
        print('#'*70)