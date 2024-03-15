import types

from Node import Node
from Node_Linear import Node_Linear
from Node_Key_Value import Node_Key_Value
import Key_Value

no_reference_types = {type(None), bool, int, float, complex, str}
no_child_references_types = {dict, types.MappingProxyType}

max_string_length = 42

type_to_node = {
    str: lambda data: Node(data), # visit as whole string, don't iterate over characters
    dict: lambda data: (
        Node_Key_Value(data, Key_Value.get_key_values(data)) 
        #if dict in no_child_references_types else Node_Linear(data, data.items()) 
        ),
    Key_Value.Key_Value: lambda data: data,
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
    dict : "dodgerblue1",
    types.MappingProxyType : "red", #"dodgerblue2", # not used
    #utils.class_type : "seagreen1",
    type: "seagreen2", # where class variable are stored
}
