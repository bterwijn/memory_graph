import utils

from HTML_Table import HTML_Table

class Node:
    node_id = 0
    
    def __init__(self, data, children=None):
        self.node_id = Node.node_id
        Node.node_id += 1
        self.data = data
        self.parent = None
        self.children = children

    def __repr__(self):
        return f'Node({self.data})'

    def get_data(self):
        return self.data

    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children
    
    def get_name(self):
        return f'node{self.node_id}'
    
    def get_html_table(self):
        html_table = HTML_Table()
        if self.children is None:
            html_table.add_string(f'{self.data}')
        else:
            html_table.add_inner_table()
            self.fill_html_table(html_table)
        return html_table
    
    def get_label(self):
        return utils.get_type_name(self.data)
    
    # -------------------- Node interface --------------------

    def do_backtrack_callback(self):
        return True
    
    def transform(self, fun):
        pass

    def visit_with_depth(self, fun):
        pass
        
    def fill_html_table(self, html_table):
        pass
