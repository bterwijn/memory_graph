from memory_graph.element_base import Element_Base
from memory_graph.element_linear import Element_Linear
from memory_graph.element_key_value import Element_Key_Value

import memory_graph.utils as utils    
import memory_graph.config as config

def data_to_element(data):
    data_type = type(data)
    if data_type in config.type_to_element: # for predefined types
        return config.type_to_element[type(data)](data)
    elif utils.has_dict_attributes(data): # for user defined classes
        return Element_Key_Value(data, utils.filter_dict_attributes(utils.get_dict_attributes(data)) )
    elif utils.is_iterable(data): # for lists, tuples, sets, ...
        return Element_Linear(data, data)
    else:
        return Element_Base(data)

def to_elements_recursive(data, parent, parent_index, known_elements):
    data_id = id(data)
    if data_id in known_elements:
        element = known_elements[data_id]
    else:
        element = data_to_element(data)
        known_elements[data_id] = element
        for index in element.get_children().indices_all():
            child = element.get_children()[index]
            child_element = to_elements_recursive(child, element, index, known_elements)
            element.get_children()[index] = child_element
    if not parent is None:
        element.add_parent_index(parent, parent_index)
    return element

def to_elements(data):
    return to_elements_recursive(data, None, None, {})
