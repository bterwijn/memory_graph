import utils

def outer_html_table(node, s, color='white'):
    #color = get_color(categorized, color)
    border = 1 #if categorized.get_parent() else 3
    return (f'<\n<TABLE BORDER="0" CELLBORDER="{border}" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X">\n' +
            s + '\n</TD></TR></TABLE>\n>')

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
    
    def get_name(self):
        return f'node{id(self.data)}'
    
    def get_html(self):
        return outer_html_table(self, f'{self.data}')
    
    def get_label(self):
        return utils.get_type_name(self.data)

    def get_edges(self):
        edges = []
        if self.children:
            print('children:', self.children)
            self.children.visit( lambda child: edges.append( (self,child) ))
        return edges
    
    def __repr__(self):
        return f'Node({self.data})'#, children={self.children})'

