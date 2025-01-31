# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Configuration file for the graph visualizer. The configuration values are set later by the 'config_default.py' file. """

max_tree_depth = None
max_missing_edges = None
max_string_length = None
graph_stability = None

not_node_types = {}
no_child_references_types = set()

type_to_node = { }

type_to_color = { }

type_to_vertical_orientation = { }

type_to_slicer = { }
