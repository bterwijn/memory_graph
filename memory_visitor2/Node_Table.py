from Node import Node
from Slicer import Slicer

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
    
class Node_Table(Node):
    slicer_width = Slicer(3,4)
    slicer_height = Slicer(4,3)

    def __init__(self, data, children, data_width=None, column_names=None, row_names=None):
        self.column_name = column_names
        self.row_name = row_names
        if data_width:
            children_sliced = [Node_Table.slicer_width.slice(children[i:i+data_width]) for i in range(0, len(children), data_width)]
        else:
            children_sliced = [Node_Table.slicer_width.slice(child) for child in children]
            if len(children_sliced) > 0:
                data_width = len(children_sliced[0])
        self.data_width = data_width
        self.data_height = len(children_sliced)
        children_sliced = Node_Table.slicer_height.slice(children_sliced,3)

        if column_names:
            self.column_names = (column_names + [' ']*(self.data_width-len(column_names)))[:self.data_width]
            self.column_names = Node_Table.slicer_width.slice(self.column_names)
        if row_names:
            self.row_names = (row_names + [' ']*(self.data_height-len(row_names)))[:self.data_height]
            self.row_names = Node_Table.slicer_height.slice(self.row_names)
        self.children = children_sliced
        super().__init__(data, children_sliced)

    def transform(self, fun):
        for row_blocks in self.children:
            for row in row_blocks:
                for column_blocks in row:
                    for i in range(len(column_blocks)):
                        column_blocks[i] = fun(column_blocks[i])

    def visit_with_depth(self, fun):
        depth = 4
        for row_blocks in self.children:
            for row in row_blocks:
                for column_blocks in row:
                    if len(column_blocks) == 0:
                        fun( (depth, None) )
                        depth = 1
                    for column in column_blocks:
                        fun( (depth,column) )
                        depth = 0
                    depth = 1
                depth = 2
            depth = 3

    def visit_with_depth_cols_rows(self, fun):
        depth = 4
        if self.column_names and self.row_names:
            fun( (depth, ' ') )
            depth=0
        if self.column_names:
            for column_blocks in self.column_names:
                if len(column_blocks) == 0:
                    fun( (depth, None) )
                    depth = 1
                for column in column_blocks:
                    fun( (depth,column) )
                    depth = 0
                depth = 1
            depth = 2
        for block_index in range(len(self.children)):
            for row_index in range(len(self.children[block_index])):
                if self.row_names:
                    fun( (depth, self.row_names[block_index][row_index]) )
                    depth=0
                for column_blocks in self.children[block_index][row_index]:
                    if len(column_blocks) == 0:
                        fun( (depth, None) )
                        depth = 1
                    for column in column_blocks:
                        fun( (depth,column) )
                        depth = 0
                    depth = 1
                depth = 2
            depth = 3

    def fill_html_table(self, html_table):
        table = HTML_Table_Helper(html_table, self.column_name, self.row_name)
        self.visit_with_depth_cols_rows(lambda depth_child : table.fill(self, depth_child[0], depth_child[1]))
    