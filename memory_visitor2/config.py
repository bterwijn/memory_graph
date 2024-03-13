from Node import Node
#from Children_Linear import Children_Linear
from Children_Key_Value import Children_Key_Value
#from Children_Table import Children_Table

no_reference_types = {type(None), bool, int, float, complex, str}

type_to_node = {
    str: lambda data: Node(data), # visit as whole string, don't iterate over characters
    dict: lambda data: Node(data, Children_Key_Value(data.items())),
    }
