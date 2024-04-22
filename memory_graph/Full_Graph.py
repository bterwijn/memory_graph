from memory_graph.Node import Node
from memory_graph.Node_Linear import Node_Linear
from memory_graph.Node_Key_Value import Node_Key_Value

import memory_graph.utils as utils    
import memory_graph.config as config
import memory_graph.config_helpers as config_helpers

class Full_Graph:

    def __init__(self, data) -> None:
        self.ids_visited = set()
        self.parents = {}
        self.children = {}
        root_id = self.build_graph_recursive(data)
        self.add_root(root_id)
        

    def __repr__(self) -> str:
        s = "Full_Graph\n=== parents:\n"
        for parent_id,child_ids in self.parents.items():
            s += f"{parent_id} : {child_ids}\n"
        s += "=== children:\n"
        for child_id,parents_indices in self.children.items():
            s += f"{child_id} : {parents_indices}\n"
        return s

    def build_graph_recursive(self, data):
        identity = id(data)
        if not identity in self.ids_visited:
            node = self.data_to_node(data)
            print("node:",node)
            self.ids_visited.add(identity)
            #node.transform(lambda x: self.build_graph_recursive(x)) # TODO, use transform?
            children = node.get_children()
            if not children is None:
                node.set_children( [self.build_graph_recursive(child) for child in children] )
            self.add(identity, node)
        else:
            print('seen:',identity, data)
        return identity
    
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

    def add(self, parent_id, node):
        self.parents[parent_id] = node
        children = node.get_children()
        if not children is None:
            for index, child in enumerate(children):
                if not child in self.children:
                    self.children[child]={}
                if not parent_id in self.children[child]:
                    self.children[child][parent_id] = []
                self.children[child][parent_id].append(index)

    def add_root(self, parent_id):
        self.children[parent_id] = {}
        self.root = parent_id

    def get_root(self):
        return self.root

    def get_children(self):
        return self.children
    
    def get_parents(self):
        return self.parents

    def get_node(self, parent):
        return self.parents[parent]
    
    def get_parents(self, child):
        return self.children[child]