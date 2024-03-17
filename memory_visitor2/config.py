import types

from Node import Node
from Node_Linear import Node_Linear
from Node_Key_Value import Node_Key_Value
from Node_Hidden import Node_Hidden
from Node_Table import Node_Table
from Slicer import Slicer

no_reference_types = {type(None), bool, int, float, complex, str}
no_child_references_types = {dict, types.MappingProxyType}

max_string_length = 42

type_to_node = {
    str: lambda data: Node(data), # visit as whole string, don't iterate over characters
    dict: lambda data: (
        Node_Key_Value(data, data.items())
            if dict in no_child_references_types else 
        Node_Linear(data, data.items()) 
        ),
    Node_Hidden: lambda data: data,
    }

type_to_color = {
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

type_to_vertical_orientation = {
}

type_to_slicer = {
    Node_Linear: (Slicer(5,5,5),),
    Node_Key_Value: (Slicer(5,5,5),),
    Node_Table: (Slicer(5,5),Slicer(5,5)),
}
