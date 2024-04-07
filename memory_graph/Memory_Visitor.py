from memory_graph.Node import Node
from memory_graph.Node_Linear import Node_Linear
from memory_graph.Node_Key_Value import Node_Key_Value

import memory_graph.utils as utils    
import memory_graph.config as config
import memory_graph.config_helpers as config_helpers


def default_backtrack_callback(node):
    print('backtrack_callback:', node)
    #node.visit_with_depth(lambda child: print('-- child:', child))

class Memory_Visitor:
    """
    Memory_Visitor visits the memory in a depth first manner starting from the 'data' root node.
    Each type is converted to a Node object using the 'data_to_node' method. After each 
    child of a node is visited (and converted to Node object), the 'backtrack_callback' is called
    to indicate it can be added to the graph.
    """
    
    def __init__(self, backtrack_callback=None):
        """
        Create a Memory_Visitor object.

        Args:
            backtrack_callback (function): Sets which callback function is called after each node is visited.
        """
        config_helpers.set_config()
        self.backtrack_callback = default_backtrack_callback if backtrack_callback is None else backtrack_callback
        self.data_ids = {}

    def visit(self, data):
        """
        Visit the memory in a depth first manner starting from the 'data' root node.
        """
        self.visit_recursive(data)

    def visit_recursive(self, data, parent_node=None):
        """
        Recursively visit the memory in a depth first manner from the 'data' node onwards,
        convert each data to node based on type, and call the backtrack_callback when backtracking. 
        The 'parent_node' is the parent of the 'data' node. The 'data_ids' dictionary is 
        used to prevent reading the same data mutliple times.
        """
        #print('visit_recursive:', data, parent_node)
        if data is self:
            return None
        data_type = type(data)
        if (parent_node != None and data_type in config.no_reference_types):
            return config.no_reference_types[data_type](data)
        if len(self.data_ids) > config.max_number_nodes:
            print(f"Memory_Visitor max_number_nodes ({config.max_number_nodes}) reached, stopping recursion.")
            return None
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
        """
        Helper function to convert 'data' to a Node object based on its type.

        Returns:
            Node: The Node object representing 'data'.
        """
        if type(data) in config.type_to_node: # for predefined types
            return config.type_to_node[type(data)](data)
        elif utils.has_dict_attributes(data): # for user defined classes
            return Node_Key_Value(data, utils.filter_dict_attributes(utils.get_dict_attributes(data)) )
        elif utils.is_iterable(data): # for lists, tuples, sets, ...
            return Node_Linear(data, data)
        return Node(data) # for int, float, str, ...

