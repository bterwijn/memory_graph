from Children import Children
from Slicer import Slicer

def new(children, line_width=None, column_names=None, row_names=None):
    return Children_Table(children, line_width, column_names, row_names) if children else None

class HTML_Table_Helper:

    def __init__(self, html_table, column_name=None, row_name=None):
        self.html_table = html_table
        self.column_name = column_name
        self.row_name = row_name
        self.row_count = 0
        self.entry_count = 0

    def fill(self, node, depth, child):
        #print('depth:', depth, 'child:', child)
        if depth == 1:
            self.html_table.add_dots()
        if depth == 2:
            self.html_table.add_new_line()
        if depth == 3:
            if self.entry_count >0:
                self.html_table.add_new_line()
            self.html_table.add_dots()
            self.html_table.add_new_line()
        if child:
            if isinstance(child, str):
                self.html_table.add_column(child)
            else:
                self.html_table.add_reference(node,child)
            self.entry_count += 1
    
class Children_Table(Children):
    slicer_width = Slicer(3,4)
    slicer_height = Slicer(4,3)

    def __init__(self, children, line_width=None, column_names=None, row_names=None):
        self.column_name = column_names
        self.row_name = row_names
        print('children:', children)
        if line_width:
            children_sliced = [Children_Table.slicer_width.slice(children[i:i+line_width]) for i in range(0, len(children), line_width)]
        else:
            children_sliced = [Children_Table.slicer_width.slice(child) for child in children]
            if len(children_sliced) > 0:
                self.line_width = len(children_sliced[0])
        print('children_sliced:', children_sliced)
        children_sliced = Children_Table.slicer_height.slice(children_sliced,3)
        print('children_sliced:', children_sliced)
        super().__init__(children_sliced)

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
        table = HTML_Table_Helper(html_table, self.column_name, self.row_name)
        self.visit_with_depth(lambda depth_child : table.fill(node, depth_child[0], depth_child[1]))
    