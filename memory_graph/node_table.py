from memory_graph.node import Node
from memory_graph.sequence import Sequence2D

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
        super().__init__(data, Sequence2D(children))

    def transform(self, fun):
        """
        Transform the children of the Node using the 'fun' function.
        """
        self.children.transform(lambda s: s.transform(fun))

    def fill_html_table(self, html_table, slices, full_graph):
        """
        Fill the html_table with the children of the Node.
        """
        children = self.children
        children_size = children.size()
        children_height = children_size[0]
        children_width = children_size[1]

        row_slices = slices.get_row_slices()
        col_slices = slices.get_col_slices()

        # row indices
        row_indices = set()
        for index in row_slices.table_iter(children_height):
            if index >= 0:
                row_indices.add(index)

        # use column indices for header row
        html_table.add_value('', border=0)
        for index in col_slices.table_iter(children_width):
            if index == -1:
                html_table.add_value('', border=0)
            else:
                html_table.add_index(index)
        html_table.add_new_line()

        # add remaing rows
        first_column = True
        for index in slices.table_iter(children_size):
            rowi, coli = index
            if first_column:
                if rowi in row_indices:
                    html_table.add_index(rowi)
                else:
                    html_table.add_value('', border=0)
                first_column = False
            if coli == -1:
                html_table.add_dots()
            elif coli == -2:
                html_table.add_new_line()
                first_column = True
            elif coli == -3:
                html_table.add_new_line()
                html_table.add_value('', border=0)
                for _ in range (html_table.get_max_column()-1):
                    html_table.add_dots()
                html_table.add_new_line()
            else:
                child = children[index]
                child_node = full_graph.get_child_node(child)
                html_table.add_entry(self, child_node)

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        return f'{self.get_type_name()}'
        #return f'{self.get_type_name()} {self.data_height}⨯{self.data_width}'
    