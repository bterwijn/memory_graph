# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Sets the default configuration values for the memory graph. """
from memory_graph.utils          import unquoted_str, full_str, html_str
from memory_graph.node_leaf      import Node_Leaf
from memory_graph.node_linear    import Node_Linear
from memory_graph.node_key_value import Node_Key_Value
from memory_graph.node_table     import Node_Table

from memory_graph.call_stack import call_stack
from memory_graph.slicer import Slicer

import memory_graph.config as config
import memory_graph.utils as utils

import types

""" Colors of the graph. """
foreground_color_light = 'black'
index_color_light = '#505050'
background_color_light = 'white'
""" Colors of different types in the graph. """
type_to_color_light = {
    # ================= singular
    type(None) : "gray",
    bool : "pink",
    int : "darkolivegreen1",
    float : "plum",
    complex : "yellow",
    str : "cyan",
    # ================= linear
    tuple : "orange",
    list : "lightcoral",
    set : "orchid1",
    frozenset : "orchid2",
    bytes : "khaki1",
    bytearray : "khaki2",
    # ================= key_value
    Node_Key_Value : "seagreen1", # for classes
    call_stack : 'khaki',
    type: "seagreen3",            # where class variables are stored
    dict : "#60a5ff",
    types.MappingProxyType : "dodgerblue2", # not used
    range : "cornsilk2",
    # ================= exception
    BaseException : "#ff6666",
}

background_color_dark = "#1d1d1d"
foreground_color_dark = "#cccccc"
index_color_dark = "#999999"
type_to_color_dark = {
    # ================= singular
    type(None) : "#646464",
    bool : "#8d646d",
    int : "#507835",
    float : "#7e4974",
    complex : "#707500",
    str : "#006f6f",
    # ================= linear
    tuple : "#956200",
    list : "#783438",
    set : "#811b7d",
    frozenset : "#6a1666",
    bytes : "#73753f",
    bytearray : "#6a6c3b",
    # ================= key_value
    Node_Key_Value : "#00905d",
    call_stack : '#7e8148',
    type: "#00784e",
    dict : "#355393",
    types.MappingProxyType : "#304a84",
    range : "#7e7d6c",
    # ================= exception
    BaseException : "#a52e37",
}

def set_colors(dark, transparent):
    if dark:
        config.foreground_color = foreground_color_dark
        config.index_color = index_color_dark
        config.background_color = background_color_dark
        config.type_to_color = type_to_color_dark
    else:
        config.foreground_color = foreground_color_light
        config.index_color = index_color_light
        config.background_color = background_color_light
        config.type_to_color = type_to_color_light
    if transparent:
        config.background_color = "transparent"

def transparent_background(transparent = None):
    if transparent is None:
        config.transparent_background = not config.transparent_background
    else:
        config.transparent_background = transparent
    set_colors(config.color_mode_dark, config.transparent_background)

def dark_mode(dark = None):
    if dark is None:
        config.color_mode_dark = not config.color_mode_dark
    else:
        config.color_mode_dark = dark
    set_colors(config.color_mode_dark, config.transparent_background)

def reset():

    set_colors(config.color_mode_dark, config.transparent_background)

    """ Reopen viewer each time show() is called, this might change window focus. """
    config.reopen_viewer = True
    
    """ The default filename to render to. """
    config.render_filename = 'memory_graph.pdf'

    """ Show the type of each node as label. """
    config.type_labels = True

    """ Determines if the filename, line number and functions name is printed on mg.block(). """
    config.block_prints_location = True

    """ The messages asking user toe press <Enter> on block(), set to None to disable.  """
    config.press_enter_message = "Press <Enter> to continue..."

    """ The maximum length of strings shown in the graph. Longer strings will be truncated. """
    config.max_string_length = 42

    """ The number of references keeping child nodes in order versus other references pulling them out. """
    config.graph_stability = 10

    """ Types that by default will be embedded in the node of their parent. """
    config.embedded_types = {
        type(None), bool, int, float, complex,
        str, full_str, unquoted_str, html_str,
        types.FunctionType,
        types.MethodType,
        classmethod,
        staticmethod,
        type(len),
    }

    """ Types that are embedded as key in a Node_Key_Value node. """
    config.embedded_key_types = {type(None), bool, int, float, complex, str}

    """ Types that will embed their children. """
    config.embedding_types = {dict, types.MappingProxyType}

    """ Types that should not show an index """
    config.no_index_types = {set, frozenset}

    """ Types that need a special conversion """
    config.type_to_string = {
        types.FunctionType: lambda data: utils.prep_str(data.__qualname__),
        types.MethodType: lambda data: utils.prep_str(data.__qualname__),
        classmethod: lambda data: utils.prep_str(data.__qualname__),
        staticmethod: lambda data: utils.prep_str(data.__qualname__),
        type(len): lambda data: utils.prep_str(data.__qualname__),
        BaseException: lambda data: utils.prep_exception_str(utils.exception_to_string(data)),
        unquoted_str: lambda data: utils.newlines_to_br(utils.html_escape(str(data))),
        full_str: lambda data: utils.newlines_to_br(utils.html_escape(str(data))),
        html_str: lambda data: str(data),
    }
    
    """ Conversion from type to Node objects. """
    config.type_to_node = {
        str: lambda data: Node_Leaf(data, data), # visit as whole string, don't iterate over characters
        call_stack: lambda data: Node_Key_Value(data, data.items()),
        type: lambda data: Node_Key_Value(data, utils.filter_type_attributes(vars(data).items())),
        range: lambda data: Node_Key_Value(data, {'start':data.start, 'stop':data.stop, 'step':data.step}.items()),
        dict: lambda data: (
            Node_Key_Value(data, utils.filter_dict(data) )
            if dict in config.embedding_types else 
            Node_Linear(data, utils.filter_dict(data) )
        ),
        BaseException: lambda data: Node_Leaf(data, data),
    }

    """ Types that will be visualized in horizontal or vertical orientation based on a True/False value.
    The 'type_to_horizontal' takes precedence over 'type_to_vertical'.
    If no boolean value is present the Node decides based on it having references."""
    config.type_to_horizontal = {}
    config.type_to_vertical = {}

    
    """ Slicer objects for different types. """
    config.type_to_slicer = {
        Node_Linear: Slicer(10, 5, 10),
        Node_Key_Value: Slicer(10, 5, 10),
        Node_Table: (Slicer(3, 2, 3), Slicer(3, 2, 3)),
    }

    """ The maximum depth of nodes in the graph. When the graph gets too big set this to a small positive number. A `✂` symbol indictes where the graph is cut short. """
    config.max_graph_depth = 1000
    config.graph_cut_symbol = '✂'
    

    """ Maximum introspection depth for different types. """
    config.type_to_depth = {
    }
    
    """ Maximum number of missing edges that are shown. """
    config.max_missing_edges = 2

    """ Font name and size used in the graph. """
    config.fontname = 'Times-Roman'
    config.fontsize = '14'

reset()
