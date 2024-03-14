from Children import Children
from Slicer import Slicer

def new(children, line_width=None):
    return Children_Table(children, line_width) if children else None

def fill_html_table_helper(node, html_table, depth, child):
    #print('depth:', depth, 'child:', child)
    if depth == 1:
        html_table.add_dots()
    if depth == 2:
        html_table.add_new_line()
    if depth == 3:
        html_table.add_new_line()
        html_table.add_dots()
        html_table.add_new_line()
    if child:
        if isinstance(child, str):
            html_table.add_column(child)
        else:
            html_table.add_reference(node,child)
    
class Children_Table(Children):
    slicer_width = Slicer([":2:","-2::"])
    slicer_height = Slicer([":2:","-2::"])

    def __init__(self, children, line_width=None):
        if line_width:
            children2d = [Children_Table.slicer_width.slice(children[i:i+line_width]) for i in range(0, len(children), line_width)]
        else:
            children2d = [Children_Table.slicer_width.slice(child) for child in children]
        super().__init__(Children_Table.slicer_height.slice(children2d,3))

    def __repr__(self):
        return f'Children_Table({self.children})'

    def transform(self, fun):
        for rows in self.children:
            for row_sliced in rows:
                for column in row_sliced:
                    for i in range(len(column)):
                        column[i] = fun(column[i])

    def visit_with_depth(self, fun):
        depth = 4
        for rows in self.children:
            for row_slice in rows:
                for column in row_slice:
                    if len(column) == 0:
                        fun( (depth, None) )
                        depth = 1
                    for column_slice in column:
                        fun( (depth,column_slice) )
                        depth = 0
                    depth = 1
                depth = 2
            depth = 3
        
    def fill_html_table(self, node, html_table):
        self.visit_with_depth(lambda depth_child : 
                              fill_html_table_helper(node, html_table,depth_child[0],depth_child[1]) )
    