import utils

class Node:
    
    def __init__(self, data, children=None):
        self.data = data
        self.parent = None
        self.children = children

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children
    
    def add_to_graph(self, graph):
        if self.children:
            #self.children.add_to_graph(graph,self)
            pass
        else:
            graph.add_node(f'node{id(self.data)}',
                           f'{self.data}',
                           utils.get_type_name(self.data))
    
    def __repr__(self):
        return f'Node({self.data})'#, children={self.children})'

