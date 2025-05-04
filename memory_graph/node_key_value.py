# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from memory_graph.node_base import Node_Base
from memory_graph.sequence import Sequence1D

import memory_graph.config_helpers as config_helpers

class Node_Key_Value(Node_Base):
    """
    Node_Key_Value (subclass of Node_Base) is a node that represents a node with key-value 
    pairs (tuples) as children. This node type mainly used for dictionaries and classes. 
    Each child is made a Hidden_Node_Base so that each tuple is not shown as a separate node 
    but instead as a key,value pair in the current node.
    """

    def __init__(self, data, children):
        """
        Create a Node_Key_Value object. Use a Slicer to slice the children so the
        Node_Base will not get too big or have too many childeren in the graph.
        """
        super().__init__(data, Sequence1D(children))
    
    def has_references(self, nodes, slices, id_to_slices):
        """
        Return if the node has references to other nodes.
        """
        for index in slices:
            child_id = id(self.children[index])
            child = nodes[child_id]
            key_id = id(child.get_children()[0])
            if key_id in nodes:
                key = nodes[key_id]
                if not key.is_hidden_node():
                    return True
            value_id = id(child.get_children()[1])
            if value_id in nodes:
                value = nodes[value_id]
                if not value.is_hidden_node():
                    return True
        return False

    def is_vertical(self, nodes, slices, id_to_slices):
        """
        Return if the node is vertical or horizontal based on the orientation of the children.
        """
        vertical = config_helpers.get_vertical_orientation(self, None)
        if vertical is None:
            vertical = not self.has_references(nodes, slices, id_to_slices)
        return vertical

    def fill_html_table(self, nodes, html_table, slices, id_to_slices):
        """
        Fill the html_table with the children of the Node_Base.
        """
        if slices is None:
            return
        vertical = self.is_vertical(nodes, slices, id_to_slices)
        if vertical:
            self.fill_html_table_vertical(html_table, nodes, slices, id_to_slices)
        else:
            self.fill_html_table_horizontal(html_table, nodes, slices, id_to_slices)

    @staticmethod
    def get_value_dashed(nodes, child, index, id_to_slices):
        grandchild = child[index]
        child_id = id(child)
        is_dashed = False
        if child_id in id_to_slices:
            slices = id_to_slices[child_id]
            if not slices is None:
                is_dashed = slices.is_dashed(index)
        return grandchild, is_dashed

    def fill_html_table_vertical(self, html_table, nodes, slices, id_to_slices):
        """
        Helper function to fill the html_table with the children of the Node_Base in vertical orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                key, is_dashed = self.get_value_dashed(nodes, child,0,id_to_slices)
                html_table.add_entry(self, nodes, key, id_to_slices, rounded=True, dashed=is_dashed)
                value, is_dashed = self.get_value_dashed(nodes, child,1,id_to_slices)
                html_table.add_entry(self, nodes, value, id_to_slices, dashed=is_dashed)
            else:
                html_table.add_dots(rounded=True)
                html_table.add_dots()
            html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, nodes, slices, id_to_slices):
        """
        Helper function to fill the html_table with the children of the Node_Base in horizontal orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                key, is_dashed = self.get_value_dashed(nodes, child,0,id_to_slices)
                html_table.add_entry(self, nodes, key, id_to_slices, rounded=True, dashed=is_dashed)
            else:
                html_table.add_dots(rounded=True)
        html_table.add_new_line()
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                value, is_dashed = self.get_value_dashed(nodes, child,1,id_to_slices)
                html_table.add_entry(self, nodes, value, id_to_slices, dashed=is_dashed)
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
