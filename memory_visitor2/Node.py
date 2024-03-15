import utils

from HTML_Table import HTML_Table


class Node:
    
    def __init__(self, data, children=None):
        self.data = data
        self.parent = None
        self.children = children

    def do_backtrack_callback(self):
        return True

    def get_data(self):
        return self.data

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children
    
    def get_name(self):
        return f'node{id(self.data)}'
    
    def get_html_table(self):
        html_table = HTML_Table()
        if self.children:
            html_table.add_inner_table()
            self.children.fill_html_table(self,html_table)
        else:
            html_table.add_string(f'{self.data}')
        return html_table
    
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

