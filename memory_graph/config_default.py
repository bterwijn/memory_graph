""" Sets the default configuration values for the memory graph. """
from memory_graph.element_base      import Element_Base
from memory_graph.element_linear    import Element_Linear
from memory_graph.element_key_value import Element_Key_Value
from memory_graph.element_table     import Element_Table

from memory_graph.slicer import Slicer

import memory_graph.config as config
import memory_graph.utils as utils

import types

""" The maximum depth of nodes in the graph. When the graph gets too big set this to a small positive number. A `★` symbol indictes where the graph is cut short.  """
config.max_tree_depth = 10

config.max_missing_edges = 3

""" The maximum length of strings shown in the graph. Longer strings will be truncated. """
config.max_string_length = 42

""" Types that by default will not have references pointing to them in the graph but instead will be visualized in the node of their parent. """
config.no_reference_types = {
    type(None), bool, int, float, complex, str,
    types.FunctionType,
    types.MethodType,
}

""" Types that will not have references pointing to their children in the graph but instead will have their children visualized in their node. """
config.no_child_references_types = {dict, types.MappingProxyType}

""" Conversion from type to Element_Base objects. """
config.type_to_element = {
    str: lambda data: Element_Base(data), # visit as whole string, don't iterate over characters
    types.FunctionType: lambda data: Element_Base(data.__qualname__),
    types.MethodType: lambda data: Element_Base(data.__qualname__),
    type: lambda data: Element_Base(str(data)),
    range: lambda data: Element_Key_Value(data, {'start':data.start, 'stop':data.stop, 'step':data.step}.items()),
    dict: lambda data: (
        Element_Key_Value(data, utils.filter_dict_attributes(data.items()) )
            if dict in config.no_child_references_types else 
        Element_Linear(data, utils.filter_dict_attributes(data.items()) )
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
    Element_Key_Value : "seagreen1", # for classes
    type: "seagreen2",            # where class variables are stored
    dict : "dodgerblue1",
    types.MappingProxyType : "dodgerblue2", # not used
    range : "cornsilk",
}

""" Types that will be visualized in vertical orientation if 'True', or horizontal orientation 
if 'False'. Otherwise the Element_Base decides based on it having references."""
config.type_to_vertical_orientation = {
}

""" Slicer objects for different types. """
config.type_to_slicer = {
    Element_Linear: Slicer(5,5,5),
    Element_Key_Value: Slicer(5,5,5),
    Element_Table: (Slicer(3,3,3), Slicer(3,3)),
}
