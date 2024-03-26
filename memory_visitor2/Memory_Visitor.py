from Node import Node
from Node_Linear import Node_Linear
from Node_Key_Value import Node_Key_Value

import utils
import config
import config_helpers


def default_backtrack_callback(node):
    print('backtrack_callback:', node)
    #node.visit_with_depth(lambda child: print('-- child:', child))

class Memory_Visitor:
    
    def __init__(self, backtrack_callback=None):
        config_helpers.set_config()
        self.backtrack_callback = default_backtrack_callback if backtrack_callback is None else backtrack_callback
        self.data_ids = {}

    def visit(self, data):
        self.visit_recursive(data, None)

    def visit_recursive(self, data, parent_node):
        #print('visit_recursive:', data, parent_node)
        if data is self:
            return None
        data_type = type(data)
        if (parent_node != None and data_type in config.no_reference_types):
            return config.no_reference_types[data_type](data)
        data_id = id(data)
        if data_id in self.data_ids:
            return self.data_ids[data_id]
        else:
            node = self.data_to_node(data)
            self.data_ids[data_id] = node
            if node is not None:
                node.set_parent(parent_node)
                node.transform(lambda child: self.visit_recursive(child, node))
                if node.do_backtrack_callback():
                    self.backtrack_callback(node)
        return node

    def data_to_node(self, data):
        if type(data) in config.type_to_node: # for predefined types
            return config.type_to_node[type(data)](data)
        elif utils.has_dict_attribute(data): # for user defined classes
            return Node_Key_Value(data, utils.get_filtered_dict_attribute(data))
        elif utils.is_iterable(data): # for lists, tuples, sets, ...
            return Node_Linear(data, data)
        return Node(data) # for int, float, str, ...

