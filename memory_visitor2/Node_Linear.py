from Node import Node
from Slicer import Slicer

def fill_html_table_helper(node, html_table, depth, child):
    #print('depth:', depth, 'child:', child)
    vertical = (node.ref_count == 0)
    if depth == 1:
        html_table.add_dots()
    if child:
        if isinstance(child, str):
            html_table.add_column(child)
            if vertical:
                html_table.add_new_line()
        else:
            html_table.add_reference(node,child)
            if vertical:
                html_table.add_new_line()
    
class Node_Linear(Node):
    slicer = Slicer(3,2,3)

    def __init__(self, data, children=None):
        super().__init__(data, Node_Linear.slicer.slice(children))

    def transform(self, fun):
        self.ref_count = 0
        for block in self.children:
            for i in range(len(block)):
                block[i] = fun(block[i])
                if not type(block[i]) is str:
                    self.ref_count += 1
    
    def visit_with_depth(self, fun):
        depth = 2
        for block in self.children:
            if len(block) == 0:
                fun( (depth, None) )
                depth = 1
            for c in block:
                fun( (depth, c) )
                depth = 0
            depth = 1
        
    def fill_html_table(self, html_table):
        self.visit_with_depth(lambda depth_child : 
                              fill_html_table_helper(self, html_table,depth_child[0],depth_child[1]) )
    