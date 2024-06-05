<<<<<<< HEAD:memory_graph/node_table.py
from memory_graph.node import Node
from memory_graph.slicer import Slicer

import memory_graph.config_helpers as config_helpers

import math

def add_name_or_index(html_table, index, names):
    """
    Helper function to add either the name of a row/column (if available) or its index to the html_table.
    """
    if names and index < len(names):
        html_table.add_entry(None, names[index], rounded=True)
    else:
        html_table.add_index(index)

class Node_Table(Node):
    """
    Node_Table (subclass of Node) is a node that represents a 2D table of data used for 
    example for Numpy arrays and Pandas DataFrames.
    """

    def __init__(self, data, children, data_width=None, row_names=None, column_names=None):
        """
        Create a Node_Table object. Use a Slicer to slice the children so the Node 
        will not get to big or have too many childeren in the graph.
        """
        slicer_height, slicer_width = config_helpers.get_slicer_2d(self, data)

        if data_width:
            sliced_children = slicer_height.slice_2d(children, data_width)
            self.data_width = data_width
        else:
            sliced_children = slicer_height.slice(children)
            self.data_width = len(children[0])
        sliced_children.transform(lambda c: slicer_width.slice(c) )
        self.data_height = sliced_children.get_original_length()

        self.row_names = row_names
        self.column_names = column_names
        super().__init__(data, sliced_children)

    def transform(self, fun):
        """
        Transform the children of the Node using the 'fun' function.
        """
        self.children.transform(lambda s: s.transform(fun))

    def fill_html_table(self, html_table):
        """
        Fill the html_table with the children of the Node.
        """
        # index on top row
        for index1, jump1, slice in self.children:
            if slice:
                html_table.add_value('', border=0)
                for index2, jump2, value in slice:
                    if jump2:
                        html_table.add_value('', border=0)
                    if value is not None:
                        add_name_or_index(html_table, index2, self.column_names)
                        #html_table.add_index(index2)
                html_table.add_new_line()
                break
        # remaining rows
        for index1, jump1, slice in self.children:
            #print('index1:',index1,'jump1:',jump1,'sliced:',slice)
            if jump1:
=======
from memory_graph.node_base import Node_Base
from memory_graph.sequence import Sequence2D
from memory_graph.list_view import List_View

class Node_Table(Node_Base):
    """
    Node_Table (subclass of Node_Base) is a node that represents a 2D table of data used for 
    example for Numpy arrays and Pandas DataFrames.
    """

    def __init__(self, data, children, data_width=None, row_names=None, col_names=None):
        """
        Create a Node_Table object. Use a Slicer to slice the children so the Node_Base 
        will not get to big or have too many childeren in the graph.
        """
        self.row_names = row_names
        self.col_names = col_names
        if data_width is None:
            super().__init__(data, Sequence2D(children))
        else:
            list_views = [List_View(children, i, i+data_width) for i in range(0,len(children),data_width)]
            super().__init__(data, Sequence2D(list_views))

    def add_index_or_name(self, html_table, index, names):
        if not names is None and index < len(names):
            html_table.add_value(names[index], rounded=1, border=1)
        else:
            html_table.add_index(index)

    def fill_html_table(self, nodes, html_table, slices, id_to_slices):
        """
        Fill the html_table with the children of the Node_Base.
        """
        if slices.is_empty():
            return
        children = self.children
        children_size = children.size()
        children_width = children_size[1]
        col_slices = slices.get_col_slices()

        # use column indices for header row
        html_table.add_value('', border=0)
        for coli in col_slices.table_iter(children_width):
            if coli == -1:
                html_table.add_value('', border=0)
            else:
                self.add_index_or_name(html_table, coli, self.col_names)
        html_table.add_new_line()

        # add remaing rows
        first_col = True
        for index in slices.table_iter(children_size):
            rowi, coli = index
            if first_col and not coli==-3:
                first_col = False
                self.add_index_or_name(html_table, rowi, self.row_names)
            if coli == -1:
                html_table.add_dots()
            elif coli == -2:
                html_table.add_new_line()
                first_col = True
            elif coli == -3:
>>>>>>> nodes:memory_graph_new/node_table.py
                html_table.add_new_line()
                html_table.add_value('', border=0)
                for _ in range (html_table.get_max_column()-1):
                    html_table.add_dots()
                html_table.add_new_line()
<<<<<<< HEAD:memory_graph/node_table.py
            if slice:
                add_name_or_index(html_table, index1, self.row_names)
                #html_table.add_index(index1)
                for index2, jump2, value in slice:
                    #print('  index2:',index2,'jump2:',jump2,'value:',value)
                    if jump2:
                        html_table.add_dots()
                    if value is not None:
                        html_table.add_entry(self, value)
                html_table.add_new_line()

    def get_label(self):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        return f'{self.get_type_name()} {self.data_height}⨯{self.data_width}'
=======
                first_col = True
            else:
                child = children[index]
                html_table.add_entry(self, nodes, child, id_to_slices, dashed=slices.is_dashed(index))

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        size = self.get_children().size()
        return f'{self.get_type_name()} {size[0]}⨯{size[1]}'
>>>>>>> nodes:memory_graph_new/node_table.py
    