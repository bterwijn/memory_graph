# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from memory_graph.node_base import Node_Base

class Node_Leaf(Node_Base):
    """
    Node_Leaf (subclass of Node_Base) is a leaf node with no children but a value.
    """

    def __init__(self, data, value):
        """
        Create a Node_Leaf object.
        """
        super().__init__(data)
        self.value = value

    def fill_html_table(self, nodes, html_table, slices, id_to_slices):
        """
        Fill the html_table with the children of the Node_Base.
        """
        html_table.add_value(self.value)
