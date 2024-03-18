from Node import Node
from Slicer import Slicer
import config_helpers
import math

class HTML_Table_Helper:

    def __init__(self, html_table, node, column_names=None, row_names=None):
        self.html_table = html_table
        self.node = node
        self.column_names = column_names
        self.row_names = row_names

    def is_rounded(self):
        return ((not self.column_names is None and self.html_table.get_row() == 0) or
                (not self.row_names is None and self.html_table.get_column() == 0))

    def fill(self, depth, child):
        #print('depth:', depth, 'child:', child)
        if depth == 1:
            self.html_table.add_dots(rounded=self.is_rounded())
        if depth == 2:
            self.html_table.add_new_line()
        if depth == 3:
            if self.html_table.get_column() >0:
                self.html_table.add_new_line()
            for _ in range(self.html_table.get_max_column()):
                self.html_table.add_dots(rounded=self.is_rounded())
            self.html_table.add_new_line()
        if child:
            if isinstance(child, str):
                self.html_table.add_column(child, rounded=self.is_rounded())
            else:
                self.html_table.add_reference(self.node, child, rounded=self.is_rounded())
    
class Node_Table(Node):

    def __init__(self, data, children, data_width=None, column_names=None, row_names=None):
        self.column_names = column_names
        self.row_names = row_names
        slicer_width, slicer_height = config_helpers.get_slicer_2d(self, data)
        print('children:',children)
        if data_width:
            children_sliced = [slicer_width.slice(children[i:i+data_width]) for i in range(0, len(children), data_width)]
            self.data_width = data_width
            self.data_height = math.ceil(len(children) / data_width)
        else:
            children_sliced = [slicer_width.slice(child) for child in children]
            self.data_height = len(children)
            self.data_width = 0 if len(children) == 0 else len(children[0])
        print('data_width:',self.data_width)
        print('data_height:',self.data_height)

        print('children_sliced1:',children_sliced)
        children_sliced = slicer_height.slice(children_sliced,3)
        print('children_sliced2:',children_sliced)
        if column_names:
            self.column_names = (column_names + [' ']*(self.data_width-len(column_names)))[:self.data_width]
            self.column_names = slicer_width.slice(self.column_names)
        if row_names:
            self.row_names = (row_names + [' ']*(self.data_height-len(row_names)))[:self.data_height]
            self.row_names = slicer_height.slice(self.row_names)
        self.children = children_sliced
        
        super().__init__(data, children_sliced, f'{self.data_width}x{self.data_height}')

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
                    row_value = None
                    if row_index < len(self.row_names[block_index]):
                        row_value = self.row_names[block_index][row_index]
                    fun( (depth, row_value) )
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
        table = HTML_Table_Helper(html_table, self, self.column_names, self.row_names)
        self.visit_with_depth_cols_rows(lambda depth_child : table.fill(depth_child[0], depth_child[1]))
    