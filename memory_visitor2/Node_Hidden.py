from Node import Node

class Node_Hidden(Node):

    def __init__(self, data, children):
        super().__init__(data, children)

    def do_backtrack_callback(self):
        return False
    
    def transform(self, fun):
        for i in range(len(self.children)):
            self.children[i] = fun(self.children[i])
        
    def visit_with_depth(self, fun):
        dept = 1
        for i in self.children:
            fun( (depth, i) )
            depth = 0
