from Node import Node
from Slicer import Slicer

def fill_html_table_helper(node, html_table, depth, child):
    #print('depth:', depth, 'child:', child)
    if depth == 1:
        html_table.add_dots()
    if child:
        key, value = child.get_children()
        if key:
            if isinstance(key, str):
                html_table.add_column(key)
            else:
                html_table.add_reference(node,key)
        if value:
            if isinstance(value, str):
                html_table.add_column(value)
            else:
                html_table.add_reference(node,value)

class Node_Key_Value(Node):
    slicer = Slicer(3,2,3)

    def __init__(self, data, children):
        super().__init__(data, Node_Key_Value.slicer.slice(children))
        
    def transform(self, fun):
        for block in self.children:
            for i in range(len(block)):
                block[i] = fun(block[i])

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
