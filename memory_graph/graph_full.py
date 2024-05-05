from memory_graph.element_base import Element_Base
from memory_graph.element_linear import Element_Linear
from memory_graph.element_key_value import Element_Key_Value
from memory_graph.sequence import Sequence1D

import memory_graph.utils as utils    
import memory_graph.config as config

class Graph_Full:

    def __init__(self, data) -> None:
        self.id_to_element = {}         # {id:Element_Base}
        self.id_to_parent_indices = {}  # {id:{id:[index]}}
        root_id = self.build_graph_recursive(data)
        self.add_root(root_id)

    def __repr__(self) -> str:
        s = "Graph_Full\n=== elements:\n"
        for element_id,element in self.id_to_element.items():
            s += f"{element_id} : {element}\n"
        s += "=== parent_indices:\n"
        for child_id,parents_indices in self.id_to_parent_indices.items():
            s += f"{child_id} : {parents_indices}\n"
        return s

    def build_graph_recursive(self, data):
        element_id = id(data)
        if not element_id in self.id_to_element:
            element = self.data_to_element(data)
            print("element:",element)
            self.id_to_element[element_id] = element
            if isinstance(element, Element_Base):
                children = element.get_children()
                if not children is None:
                    for index in children.indices_all():
                        self.add_child(element_id, self.build_graph_recursive(children[index]), index)
        return element_id

    def add_child(self, element_id, child_id, index):
        if not child_id in self.id_to_parent_indices:
            self.id_to_parent_indices[child_id]={}
        if not element_id in self.id_to_parent_indices[child_id]:
            self.id_to_parent_indices[child_id][element_id] = []
        self.id_to_parent_indices[child_id][element_id].append(index)

    def data_to_element(self, data):
        """
        Helper function to convert 'data' to a Element_Base object based on its type.

        Returns:
            Element_Base: The Element_Base object representing 'data'.
        """
        data_type = type(data)
        if data_type in config.type_to_element: # for predefined types
            return config.type_to_element[type(data)](data)
        elif utils.has_dict_attributes(data): # for user defined classes
            return Element_Key_Value(data, utils.filter_dict_attributes(utils.get_dict_attributes(data)) )
        elif utils.is_iterable(data): # for lists, tuples, sets, ...
            return Element_Linear(data, data)
        elif (not data_type in config.no_reference_types): # for reference types
            return Element_Base(data)
        return data # for int, float, ...

    def add_root(self, element_id):
        self.id_to_parent_indices[element_id] = {}
        self.root_id = element_id

    def size(self):
        return len(self.id_to_element)

    def get_root_id(self):
        return self.root_id

    def get_all_element_ids(self):
        return self.id_to_element

    def get_element_by_id(self, element_id):
        return self.id_to_element[element_id]

    def get_data(self, element):
        if isinstance(element, Element_Base):
            return element.get_data()
        return element

    def get_children(self, element):
        if isinstance(element, Element_Base):
            return element.get_children()
        return None

    def get_parent_indices_by_id(self, element_id):
        if element_id in self.id_to_parent_indices:
            return self.id_to_parent_indices[element_id]
        return {}
