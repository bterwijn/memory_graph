
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
    
    def __repr__(self):
        return f'Node({self.data})'#, children={self.children})'

