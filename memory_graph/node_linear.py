from memory_graph.node import Node
from memory_graph.sequence import Sequence1D

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
        super().__init__(data, Sequence1D(children))

    def transform(self, fun):
        """
        Transform the children of the Node using the 'fun' function.
        """
        self.children.transform(fun)
        
    def fill_html_table(self, html_table, slices, full_graph):
        """
        Fill the html_table with the children of the Node.
        """
        #has_nodes = self.children.check_condition_on_children(lambda c: isinstance(c, Node))
        vertical = False #config_helpers.get_vertical_orientation(self, not has_nodes)
        if vertical:
            self.fill_html_table_vertical(html_table, slices, full_graph)
        else:
            self.fill_html_table_horizontal(html_table, slices, full_graph)

    def fill_html_table_vertical(self, html_table, slices, full_graph):
        """
        Helper function to fill the html_table with the children of the Node in vertical orientation.
        """
        children = self.children
        for index in slices.table_iter(children.size()):
            if index>=0:
                html_table.add_index(index)
                child = children[index]
                child_node = full_graph.get_child_node(child)
                html_table.add_entry(self, child_node)
                html_table.add_new_line()
            else:
                html_table.add_value('', border=0)
                html_table.add_dots()
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, slices, full_graph):
        """
        Helper function to fill the html_table with the children of the Node in horizontal orientation.
        """
        children = self.children
        for index in slices.table_iter(children.size()):
            if index>=0:
                html_table.add_index(index)
            else:
                html_table.add_value('', border=0)
        html_table.add_new_line()
        for index in slices.table_iter(children.size()):
            if index>=0:
                child = children[index]
                child_node = full_graph.get_child_node(child)
                html_table.add_entry(self, child_node)
            else:
                html_table.add_dots()