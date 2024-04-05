""" This module provides helper functions to access the configuration of the memory graph. """
from memory_graph.Slicer import Slicer

import memory_graph.config as config
import memory_graph.utils as utils

type_to_color = None
type_to_vertical_orientation = None
type_to_slicer = None

def set_config(colors=None, vertical_orientations=None, slicers=None):
    global type_to_color
    global type_to_vertical_orientation
    global type_to_slicer
    type_to_color = config.type_to_color.copy()
    type_to_vertical_orientation = config.type_to_vertical_orientation.copy()
    type_to_slicer = config.type_to_slicer.copy()
    if colors:
        type_to_color                |= colors
    if vertical_orientations:
        type_to_vertical_orientation |= vertical_orientations
    if slicers:
        type_to_slicer               |= slicers

def get_property(data_id, data_type, node_type, dictionary, default):
    if data_id in dictionary:
        return dictionary[data_id]
    if data_type in dictionary:
        return dictionary[data_type]
    if node_type in dictionary:
        return dictionary[node_type]
    return default

def get_color(node, default='white'):
    return get_property(id(node.get_data()), 
                        type(node.get_data()),
                        type(node), 
                        type_to_color, 
                        default)
    
def get_vertical_orientation(node, default):
    return get_property(id(node.get_data()), 
                        type(node.get_data()),
                        type(node),  
                        type_to_vertical_orientation, 
                        default)

def get_slicer_1d(node, data, default=Slicer(10,5,10)):
    slicer = get_property(id(data),
                        type(data),
                        type(node), 
                        type_to_slicer, 
                        default)
    if type(slicer) is Slicer:
        return slicer
    if utils.is_iterable(slicer):
        return next(iter(slicer))
    return default

def get_slicer_2d(node, data, default=Slicer(5,5)):
    slicer = get_property(id(data),
                        type(data),
                        type(node), 
                        type_to_slicer, 
                        default)
    if type(slicer) is Slicer:
        return slicer, slicer
    if len(slicer) == 2:
        return slicer
    return default, default
