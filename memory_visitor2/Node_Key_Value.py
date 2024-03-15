from Node import Node
from Slicer import Slicer

class HTML_Table_Helper:

    def __init__(self, html_table, node):
        self.html_table = html_table
        self.node = node
        self.elements = []
        self.ref_count = 0

    def fill(self, depth, child):
        #print('depth:', depth, 'child:', child)
        if depth == 1:
            self.elements.append('dots')
        if child:
            key, value = child.get_children()
            if not type(key) is str:
                self.ref_count += 1
            if not type(value) is str:
                self.ref_count += 1
            self.elements.append(child)

    def fill_elements(self):
        vertical = (self.ref_count == 0)
        print('vertical:', vertical)
        if vertical:
            for e in self.elements:
                if e == 'dots':
                    self.html_table.add_dots()
                    self.html_table.add_dots()
                else:
                    key, value = e.get_children()
                    if key:
                        if isinstance(key, str):
                            self.html_table.add_column(key,rounded=True)
                        else:
                            self.html_table.add_reference(self.node,key,rounded=True)
                    if value:
                        if isinstance(value, str):
                            self.html_table.add_column(value)
                        else:
                            self.html_table.add_reference(self.node,value)
                    self.html_table.add_new_line()
        else:
            for e in self.elements:
                if e == 'dots':
                    self.html_table.add_dots()
                else:
                    key, value = e.get_children()
                    if key:
                        if isinstance(key, str):
                            self.html_table.add_column(key,rounded=True)
                        else:
                            self.html_table.add_reference(self.node,key,rounded=True)
            self.html_table.add_new_line()
            for e in self.elements:
                if e == 'dots':
                    self.html_table.add_dots()
                else:
                    key, value = e.get_children()
                    if value:
                        if isinstance(value, str):
                            self.html_table.add_column(value)
                        else:
                            self.html_table.add_reference(self.node,value)

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
        table = HTML_Table_Helper(html_table,self)
        self.visit_with_depth(lambda depth_child : table.fill(depth_child[0], depth_child[1]) )
        table.fill_elements()
