# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" This module provides helper functions to access the configuration of the memory graph. """
from memory_graph.slicer import Slicer

import memory_graph.config as config

type_to_color = None
type_to_vertical = None
type_to_slicer = None

def set_config(colors=None, verticals=None, slicers=None):
    global type_to_color
    global type_to_vertical
    global type_to_slicer
    type_to_color = config.type_to_color.copy()
    type_to_vertical = config.type_to_vertical.copy()
    type_to_slicer = config.type_to_slicer.copy()
    if colors:
        type_to_color.update(colors)
    if verticals:
        type_to_vertical.update(verticals)
    if slicers:
        type_to_slicer.update(slicers)

def get_property(data_id, data_type, node_type, dictionary, default):
    if data_id in dictionary:
        return dictionary[data_id]
    if data_type in dictionary:
        return dictionary[data_type]
    if node_type in dictionary:
        return dictionary[node_type]
    return default

def get_color(node, default='white'):
    return get_property(node.get_id(),
                        node.get_type(),
                        type(node),
                        type_to_color, 
                        default)
    
def get_vertical(node, default):
    return get_property(node.get_id(),
                        node.get_type(),
                        type(node),
                        type_to_vertical, 
                        default)

def get_slicer(node, data, default=Slicer(3,2,3)):
    return get_property(id(data),
                        type(data),
                        type(node), 
                        type_to_slicer, 
                        default)
