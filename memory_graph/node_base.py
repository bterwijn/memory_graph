# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph.utils as utils
import memory_graph.config as config
import memory_graph.config_helpers as config_helpers
from memory_graph.sequence import Sequence1D

from abc import ABC, abstractmethod

class Node_Base(ABC):
    """
    Node_Base represents a node in the memory graph. This base class has different subclasses for different types of nodes.
    """
    
    def __init__(self, data, children=None):
        """
        Create a Node_Base object.
        """
        self.data = data
        self.children = Sequence1D([]) if children is None else children
        self.parent_indices = {}

    def __repr__(self):
        """
        Return a string representation of the node showing the original data represented by the node.
        """
        return f'{self.get_type_name()}'

    def add_parent_index(self, parent, parent_index):
        """
        Add a parent to the node.
        """
        if not parent in self.parent_indices:
            self.parent_indices[parent] = []
        self.parent_indices[parent].append(parent_index)

    def is_root(self):
        """
        Return if the node is the root node.
        """
        return len(self.parent_indices) == 0

    def get_parent_indices(self):
        return self.parent_indices

    def get_id(self):
        """
        Return the id of the node.
        """
        return id(self.data)

    def __eq__(self, other):
        """
        Return if the node is equal to another node.
        """
        return self.get_id() == other.get_id()
    
    def __hash__(self):
        """
        Return the hash of the node.
        """
        return self.get_id()

    def get_data(self):
        """
        Return the original data represented by the node.
        """
        return self.data
    
    def get_type(self):
        """
        Return the type of the data represented by the node.
        """
        return type(self.data)
    
    def get_type_name(self):
        """
        Return the name of the type of the data represented by the node.
        """
        return utils.get_type_name(self.data)

    def get_children(self):
        """
        Return the children of the node. Initially the children are raw data, but 
        later they too are converted to Node_Base by the Memory_visitor using the Node_Base 'transform' method.
        """
        return self.children

    def get_name(self):
        """
        Return a unique name for the node.
        """
        return f'node{self.get_id()}'

    def get_html_table(self, nodes, slices, id_to_slices):
        """
        Return the HTML_Table object that determines how the node is visualized in the graph.
        """
        from memory_graph.html_table import HTML_Table
        import memory_graph.node_base
        html_table = HTML_Table()
        self.fill_html_table(nodes, html_table, slices, id_to_slices)
        return html_table
    
    def get_slicer(self):
        return config_helpers.get_slicer(self, self.get_data())
    
    def is_hidden_node(self):
        """
        Return if the node is a hidden node in the graph.
        """
        from memory_graph.node_key_value import Node_Key_Value
        if self.get_type() is tuple:
            parent_indices = self.get_parent_indices()
            if len(parent_indices) == 1:
                first_parent = next(iter(parent_indices))
                if type(first_parent) is Node_Key_Value:
                    return True
        return False

    # -------------------- Node_Base interface, overriden by subclasses --------------------

    @abstractmethod
    def fill_html_table(self, html_table, slices, id_to_slices):
        """
        Fill the HTML_Table object with each child of the node.
        """
        pass

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        return self.get_type_name()
