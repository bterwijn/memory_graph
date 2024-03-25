import config
import types

from Node import Node
from Node_Linear import Node_Linear
from Node_Key_Value import Node_Key_Value
from Node_Hidden import Node_Hidden
from Node_Table import Node_Table
from Slicer import Slicer

from Memory_Graph import Memory_Graph
from Memory_Visitor import Memory_Visitor

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
config.no_child_references_types = {dict, types.MappingProxyType}

config.max_string_length = 42

config.type_to_node = {
    str: lambda data: Node(data), # visit as whole string, don't iterate over characters
    types.FunctionType: lambda data: Node(data.__qualname__),
    types.MethodType: lambda data: Node(data.__qualname__),
    Memory_Graph : Node('Memory_Graph'),
    Memory_Visitor : Node('Memory_Visitor'),
    dict: lambda data: (
        Node_Key_Value(data, data.items())
            if dict in config.no_child_references_types else 
        Node_Linear(data, data.items()) 
        ),
    Node_Hidden: lambda data: data,
    }

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
}

config.type_to_vertical_orientation = {
}

config.type_to_slicer = {
    Node_Linear: Slicer(5,5,5),
    Node_Key_Value: Slicer(5,5,5),
    Node_Table: (Slicer(3,3,3), Slicer(3,3)),
}
