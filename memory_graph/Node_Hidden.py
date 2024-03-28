from memory_graph.Node import Node

class Node_Hidden(Node):

    def __init__(self, data, children):
        super().__init__(data, children)

    def do_backtrack_callback(self):
        return False
    
    def transform(self, fun):
        self.children = [fun(i) for i in self.children]
