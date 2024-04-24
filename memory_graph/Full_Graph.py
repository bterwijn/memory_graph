from memory_graph.Node import Node
from memory_graph.Node_Linear import Node_Linear
from memory_graph.Node_Key_Value import Node_Key_Value

import memory_graph.utils as utils    
import memory_graph.config as config

class Full_Graph:

    def __init__(self, data) -> None:
        self.id_to_node = {}            # {id:Node}
        self.id_to_parent_indices = {}  # {id:{id:[index]}}
        root_id = self.build_graph_recursive(data)
        self.add_root(root_id)

    def __repr__(self) -> str:
        s = "Full_Graph\n=== nodes:\n"
        for node_id,node in self.id_to_node.items():
            s += f"{node_id} : {node}\n"
        s += "=== parent_indices:\n"
        for child_id,parents_indices in self.id_to_parent_indices.items():
            s += f"{child_id} : {parents_indices}\n"
        return s

    def build_graph_recursive(self, data):
        node_id = id(data)
        if not node_id in self.id_to_node:
            node = self.data_to_node(data)
            print("node:",node)
            self.id_to_node[node_id] = node
            children = node.get_children()
            if not children is None:
                for index in range(len(children)):
                    child_id = self.build_graph_recursive(children[index])
                    children[index] = child_id
                    self.add_child(node_id, child_id, index)
        else:
            print('seen:',node_id, data)
        return node_id

    def add_child(self, node_id, child_id, index):
        if not child_id in self.id_to_parent_indices:
            self.id_to_parent_indices[child_id]={}
        if not node_id in self.id_to_parent_indices[child_id]:
            self.id_to_parent_indices[child_id][node_id] = []
        self.id_to_parent_indices[child_id][node_id].append(index)

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

    def add_root(self, node_id):
        self.id_to_parent_indices[node_id] = {}
        self.root_id = node_id

    def get_root_id(self):
        return self.root_id

    def get_node_ids(self):
        return self.id_to_node

    def get_node(self, node_id):
        return self.id_to_node[node_id]
    
    def get_parents(self, node_id):
        return self.id_to_parent_indices[node_id]