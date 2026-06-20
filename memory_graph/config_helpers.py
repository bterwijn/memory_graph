# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" This module provides helper functions to access the configuration of the memory graph. """
import memory_graph.utils as utils
from memory_graph.slicer import Slicer
import memory_graph.config as config
import memory_graph.utils as utils

def get_property(data_id, data_types, node_type, dictionary, default):
    if data_id in dictionary:
        return dictionary[data_id]
    for data_type in data_types:
        if data_type in dictionary:
            return dictionary[data_type]
    if node_type in dictionary:
        return dictionary[node_type]
    return default

def get_data_to_node(data, default=None):
    return get_property(id(data),
                        utils.get_all_types(data),
                        None,
                        config.type_to_node, 
                        default )

def is_property(data_id, data_types, node_type, types_set):
    if data_id in types_set:
        return True
    for data_type in data_types:
        if data_type in types_set:
            return True
    if node_type in types_set:
        return True
    return False

def is_embedded_type(data):
    return is_property(id(data),
                       utils.get_all_types(data),
                       None,
                       config.embedded_types )

def default_to_string(data):
    """ Convert data to string. """
    try:
        if isinstance(data, str):
            s = data
        else:
            s = str(data)
        return 
    except Exception as e:
        s = 'no stringification, '+ type(e).__name__ +': '+ str(e)
    return utils.prep_str(s)

def get_to_string(data, default=lambda d: default_to_string(d)):
    return get_property(id(data),
                        utils.get_all_types(data),
                        None,
                        config.type_to_string, 
                        default )

def get_node_color(node, default=config.background_color):
    return get_property(node.get_id(),
                        utils.get_all_types(node.get_data()),
                        type(node),
                        config.type_to_color, 
                        default)
    
def get_node_vertical(node, default):
    horizontal = get_property(node.get_id(),
                              utils.get_all_types(node.get_data()),
                              type(node),
                              config.type_to_horizontal,
                              None)
    if isinstance(horizontal, bool):
        return not horizontal
    return get_property(node.get_id(),
                        utils.get_all_types(node.get_data()),
                        type(node),
                        config.type_to_vertical,
                        default)

def get_node_slicer(node, data, default=Slicer(3,2,3)):
    return get_property(id(data),
                        utils.get_all_types(node.get_data()),
                        type(node), 
                        config.type_to_slicer, 
                        default)
