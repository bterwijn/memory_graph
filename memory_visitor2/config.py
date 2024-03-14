import types

from Node import Node
#from Children_Linear import Children_Linear
from Children_Key_Value import Children_Key_Value
#from Children_Table import Children_Table

no_reference_types = {type(None), bool, int, float, complex, str}

max_string_length = 42

type_to_node = {
    str: lambda data: Node(data), # visit as whole string, don't iterate over characters
    dict: lambda data: Node(data, Children_Key_Value(data.items())),
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
