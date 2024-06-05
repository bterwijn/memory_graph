<<<<<<< HEAD:memory_graph/node_linear.py
from memory_graph.node import Node
from memory_graph.slicer import Slicer

import memory_graph.config_helpers as config_helpers

class Node_Linear(Node):
    """
    Node_Linear (subclass of Node) is a node that represents a linear sequence 
=======
from memory_graph.node_base import Node_Base
from memory_graph.sequence import Sequence1D

import memory_graph.config_helpers as config_helpers

class Node_Linear(Node_Base):
    """
    Node_Linear (subclass of Node_Base) is a node that represents a linear sequence 
>>>>>>> nodes:memory_graph_new/node_linear.py
    of data used for most iterable type like list, tuple, set, etc.
    """

    def __init__(self, data, children=None):
        """
        Create a Node_Linear object. Use a Slicer to slice the children so the 
<<<<<<< HEAD:memory_graph/node_linear.py
        Node will not get to big or have too many childeren in the graph.
        """
        slicer = config_helpers.get_slicer_1d(self, data)
        sliced_children = slicer.slice(children)
        super().__init__(data, sliced_children)

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
=======
        Node_Base will not get to big or have too many childeren in the graph.
        """
        super().__init__(data, Sequence1D(children))
    
    def has_references(self, nodes, slices):
        """
        Return if the node has references to other nodes.
        """
        for index in slices:
            child_id = id(self.children[index])
            if child_id in nodes:
                child = nodes[child_id]
                if not child.is_hidden_node():
                    return True
        return False

    def is_vertical(self, nodes, slices, id_to_slices):
        """
        Return if the node is vertical or horizontal based on the orientation of the children.
        """
        vertical = config_helpers.get_vertical_orientation(self, None)
        if vertical is None:
            vertical = not self.has_references(nodes, slices)
        return vertical

    def fill_html_table(self, nodes, html_table, slices, id_to_slices):
        """
        Fill the html_table with the children of the Node_Base.
        """
        if self.is_vertical(nodes, slices, id_to_slices):
            self.fill_html_table_vertical(html_table, nodes, slices, id_to_slices)
        else:
            self.fill_html_table_horizontal(html_table, nodes, slices, id_to_slices)

    def fill_html_table_vertical(self, html_table, nodes, slices, id_to_slices):
        """
        Helper function to fill the html_table with the children of the Node_Base in vertical orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                html_table.add_index(index)
                child = self.children[index]
                html_table.add_entry(self, nodes, child, id_to_slices, dashed=slices.is_dashed(index))
                html_table.add_new_line()
            else:
                html_table.add_value('', border=0)
                html_table.add_dots()
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, nodes, slices, id_to_slices):
        """
        Helper function to fill the html_table with the children of the Node_Base in horizontal orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                html_table.add_index(index)
            else:
                html_table.add_value('', border=0)
        html_table.add_new_line()
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                html_table.add_entry(self, nodes, child, id_to_slices, dashed=slices.is_dashed(index))
            else:
                html_table.add_dots()

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        type_name = self.get_type_name()
        if slices is None:
            return f'{type_name}'
        size = self.get_children().size()
        s = slices.get_slices()
        if len(s) == 1:
            if s[0][1] - s[0][0] == size:
                return f'{type_name}'
        return f'{type_name} {size}'
        
>>>>>>> nodes:memory_graph_new/node_linear.py
