# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Configuration file for the graph visualizer. The configuration values are set later by the 'config_default.py' file. """

reopen_viewer = None
render_filename = None

block_prints_location = None
press_enter_message = None

max_string_length = None
graph_stability = None

embedded_types = set()
not_node_types = embedded_types # deprecated

embedded_key_types = {}

embedding_types = set()
no_child_references_types = embedding_types # deprecated

type_to_string = { }

def to_string(data):
    """ Convert data to string. """
    data_type = type(data)
    if data_type in type_to_string:
        return type_to_string[data_type](data)
    return str(data)

type_to_node = { }

type_to_color = { }

type_to_vertical = { }

type_to_slicer = { }

max_graph_depth = None
graph_cut_symbol = None
max_missing_edges = None

type_to_depth = { }
