from constant import T_INT, T_FLOAT

class Node:

    def __init__(self, token=None):

        self.left = None
        self.right = None
        self.token = token

    def insert(self, token):
        if self.token != None:
            if self.right is None:
                self.right = Node(token)
            else:
                self.right.insert(token)
            if self.left is None:
                self.left = Node(token)
            else:
                self.left.insert(token)
        else:
            self.token = token

    def printTree(self):
        if self.left:
            self.left.printTree()
        print(self.token)
        if self.right:
            self.right.printTree()

    def preorderTraversal(self, root):
        res = []
        if root:
            res.append(root.token)
            res = res + self.preorderTraversal(root.left)
            res = res + self.preorderTraversal(root.right)
        return res
