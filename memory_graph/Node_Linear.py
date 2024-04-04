from memory_graph.Node import Node
from memory_graph.Slicer import Slicer

import memory_graph.config_helpers as config_helpers

class Node_Linear(Node):
    """
    Node_Linear (subclass of Node) is a node that represents a linear sequence 
    of data used for most iterable type like list, tuple, set, etc.
    """

    def __init__(self, data, children=None):
        """
        Create a Node_Linear object. Use a Slicer to slice the children so the 
        Node will not get to big or have too many childeren in the graph.
        """
        slicer = config_helpers.get_slicer_1d(self, data)
        sliced_children = slicer.slice(children)
        super().__init__(data, sliced_children, sliced_children.get_original_length())

    def transform(self, fun):
        """
        Transform the children of the Node using the 'fun' function.
        """
        self.children.transform(fun)
        
    def fill_html_table(self, html_table):
        """
        Fill the html_table with the children of the Node.
        """
        has_nodes = self.children.check_condition_on_children(lambda c: isinstance(c, Node))
        vertical = config_helpers.get_vertical_orientation(self, not has_nodes)
        if vertical:
            self.fill_html_table_vertical(html_table)
        else:
            self.fill_html_table_horizontal(html_table)

    def fill_html_table_vertical(self, html_table):
        """
        Helper function to fill the html_table with the children of the Node in vertical orientation.
        """
        for index, jump, value in self.children:
            if jump:
                html_table.add_entry(self, '', border=0)
                html_table.add_dots()
                html_table.add_new_line()
            if value is not None:
                html_table.add_index(index)
                html_table.add_entry(self, value)
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table):
        """
        Helper function to fill the html_table with the children of the Node in horizontal orientation.
        """
        for index, jump, value in self.children:
            if jump:
                html_table.add_entry(self, '', border=0)
            if value is not None:
                html_table.add_index(index)
        html_table.add_new_line()
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots()
            if value is not None:
                html_table.add_entry(self, value)
