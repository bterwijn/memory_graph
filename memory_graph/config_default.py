""" Sets the default configuration values for the memory graph. """
from memory_graph.Node import Node
from memory_graph.Node_Linear import Node_Linear
from memory_graph.Node_Key_Value import Node_Key_Value
from memory_graph.Node_Hidden import Node_Hidden
from memory_graph.Node_Table import Node_Table
from memory_graph.Slicer import Slicer

import memory_graph.config as config
import memory_graph.utils as utils

import types

""" Types that by default will not have references pointing to them in the graph but instead will be visualized in the node of their parent. """
config.no_reference_types = {
    type(None) : lambda d: "None",  # so None can be used to indicate no value
    bool : lambda d: d, 
    int : lambda d: d, 
    float : lambda d: d, 
    complex : lambda d: d, 
    str : lambda d: d,
    types.FunctionType : lambda d: str(d.__qualname__),
    types.MethodType  : lambda d: str(d.__qualname__),
}

""" Types that will not have references pointing to their children in the graph but instead will have their children visualized in their node. """
config.no_child_references_types = {dict, types.MappingProxyType}

config.max_string_length = 42
config.max_number_nodes = 1000

""" Conversion from type to Node objects. """
config.type_to_node = {
    str: lambda data: Node(data), # visit as whole string, don't iterate over characters
    range: lambda data: Node_Key_Value(data, {'start':data.start, 'stop':data.stop, 'step':data.step}.items()),
    types.FunctionType: lambda data: Node(data.__qualname__),
    types.MethodType: lambda data: Node(data.__qualname__),
    dict: lambda data: (
        Node_Key_Value(data, utils.filter_dict_attributes(data.items()) )
            if dict in config.no_child_references_types else 
        Node_Linear(data, utils.filter_dict_attributes(data.items()) ) 
        ),
    Node_Hidden: lambda data: data,
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
    type: "seagreen2",            # where class variables are stored
    dict : "dodgerblue1",
    types.MappingProxyType : "dodgerblue2", # not used
    range : "cornsilk",
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
