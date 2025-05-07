# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Sets the default configuration values for the memory graph. """
from memory_graph.node_leaf      import Node_Leaf
from memory_graph.node_linear    import Node_Linear
from memory_graph.node_key_value import Node_Key_Value
from memory_graph.node_table     import Node_Table

from memory_graph.call_stack import call_stack
from memory_graph.slicer import Slicer

import memory_graph.config as config
import memory_graph.utils as utils

import types

""" The maximum depth of nodes in the graph. When the graph gets too big set this to a small positive number. A `✂` symbol indictes where the graph is cut short. """
config.max_graph_depth = 12
config.graph_cut_symbol = '✂'
config.max_missing_edges = 3

""" The maximum length of strings shown in the graph. Longer strings will be truncated. """
config.max_string_length = 42

""" The number of references keeping child nodes in order versus other references pullen them out. """
config.graph_stability = 10

""" Types that by default will not have references pointing to them in the graph but instead will be visualized in the node of their parent. """
config.not_node_types = {
    type(None), bool, int, float, complex, str,
    types.FunctionType,
    types.MethodType,
    classmethod,
    staticmethod,
}

""" Types that will not have references pointing to their children in the graph but instead will have their children visualized in their node. """
config.no_child_references_types = {dict, types.MappingProxyType}

""" Types that need an special conversion """
config.type_to_string = {
    types.FunctionType: lambda data: data.__qualname__,
    types.MethodType: lambda data: data.__qualname__,
    classmethod: lambda data: data.__qualname__,
    staticmethod: lambda data: data.__qualname__,
}

""" Conversion from type to Node objects. """
config.type_to_node = {
    str: lambda data: Node_Leaf(data, data), # visit as whole string, don't iterate over characters
    call_stack: lambda data: Node_Key_Value(data, data.items()),
    type: lambda data: Node_Key_Value(data, utils.filter_type_attributes(vars(data).items())),
    range: lambda data: Node_Key_Value(data, {'start':data.start, 'stop':data.stop, 'step':data.step}.items()),
    dict: lambda data: (
        Node_Key_Value(data, utils.filter_dict(data) )
            if dict in config.no_child_references_types else 
        Node_Linear(data, utils.filter_dict(data) )
        ),
    }

""" Colors of different types in the graph. """
config.type_to_color = {
    # ================= singular
    type(None) : "gray",
    bool : "pink",
    int : "green",
    float : "violetred1",
    complex : "yellow",
    str : "cyan",
    # ================= linear
    tuple : "orange",
    list : "lightcoral",
    set : "orchid1",
    frozenset : "orchid2",
    bytes : "khaki1",
    bytearray : "khaki2",
    # ================= key_value
    Node_Key_Value : "seagreen1", # for classes
    call_stack : 'khaki',
    type: "seagreen3",            # where class variables are stored
    dict : "dodgerblue1",
    types.MappingProxyType : "dodgerblue2", # not used
    range : "cornsilk2",
}

""" Types that will be visualized in vertical orientation if 'True', or horizontal orientation 
if 'False'. Otherwise the Node decides based on it having references."""
config.type_to_vertical_orientation = {
}

""" Slicer objects for different types. """
config.type_to_slicer = {
    Node_Linear: Slicer(5,5,5),
    Node_Key_Value: Slicer(5,5,5),
    Node_Table: (Slicer(3,3,3), Slicer(3,3)),
}
