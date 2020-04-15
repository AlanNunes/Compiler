import uuid
class SymbolTable:
    def __init__(self, scope=None, parent=None):
        self.scope = scope if scope else uuid.uuid1()
        self.parent = None if parent == None else parent
        self.entries = []

    def insert(self, id, type, val):
        if self.getEntry(id):
            return False
        self.entries.append({"id": id, "type": type, "val": val})
        return True

    def lookup(self, id):
        entr = next((item for item in self.entries if item["id"] == id), None)
        if entr:
            return [entr["val"], True]
        if self.parent:
            entr = self.parent.lookup(id)
        if not entr:
            return [None, False]
        return entr

    def update(self, id, val, type=None):
        entr = self.getEntry(id)
        if entr:
            if type:
                entr.update({"id": id, "type": type, "val": val})
            else:
                type = entr["type"]
                entr.update({"id": id, "type": type, "val": val})
            return True
        if self.parent:
            entr = self.parent.update(id, val, type)
        return True if entr else False

    def getEntry(self, id):
        return next((item for item in self.entries if item["id"] == id), None)
