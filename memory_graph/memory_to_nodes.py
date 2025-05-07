# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from memory_graph.node_leaf import Node_Leaf
from memory_graph.node_linear import Node_Linear
from memory_graph.node_key_value import Node_Key_Value

import memory_graph.utils as utils    
import memory_graph.config as config

import graphviz

def read_nodes(data):

    def data_to_node(data_type, data):
        if data_type in config.type_to_node: # for predefined types
            return config.type_to_node[data_type](data)
        elif utils.has_dict_attributes(data): # for user defined classes
            return Node_Key_Value(data, utils.filter_dict(utils.get_dict_attributes(data)) )
        elif utils.is_finite_iterable(data): # for lists, tuples, sets, ...
            return Node_Linear(data, data)
        else:
            return Node_Leaf(data, data)

    def memory_to_nodes_recursive(nodes, data, parent, parent_index):
        data_type = type(data)
        if not data_type in config.not_node_types or parent is None:
            data_id = id(data)
            if data_id in nodes:
                node = nodes[data_id]
            else:
                node = data_to_node(data_type, data)
                nodes[data_id] = node
                for index in node.get_children().indices_all():
                    child = node.get_children()[index]
                    memory_to_nodes_recursive(nodes, child, node, index)
            if not parent is None:
                node.add_parent_index(parent, parent_index)

    nodes = {}
    memory_to_nodes_recursive(nodes, data, None, None)
    root_id = id(data)
    return nodes, root_id

# --------------------------------------------------------------------------------------------

def slice_nodes(nodes, root_id, max_graph_depth):

    def slice_nodes_recursive(nodes, node_id, id_to_slices, max_graph_depth):
        if max_graph_depth == 0 or node_id in id_to_slices:
            return
        if node_id in nodes:
            node = nodes[node_id]
            children = node.get_children()
            if children.is_empty():
                id_to_slices[node_id] = None
            else:
                slicer = node.get_slicer()
                slices = children.slice(slicer)
                id_to_slices[node_id] = slices
                if not node.is_hidden_node():
                    max_graph_depth -= 1
                for index in slices:
                    slice_nodes_recursive(nodes, id(children[index]), id_to_slices, max_graph_depth)
    id_to_slices = {}
    slice_nodes_recursive(nodes, root_id, id_to_slices, max_graph_depth)
    return id_to_slices

# --------------------------------------------------------------------------------------------

def add_parent_indices(nodes, type_to_parent_indices, id_to_slices, max_missing_edges):
    #print('add_parent_indices type_to_parent_indices:',type_to_parent_indices)
    for _, parent_indices in type_to_parent_indices.items():
        dashed = len(parent_indices) > max_missing_edges
        for parent, index in parent_indices[0:max_missing_edges]:
            new_parent = False
            parent_id = parent.get_id()
            if not parent_id in id_to_slices:
                new_parent = True
                id_to_slices[parent_id] = parent.get_children().empty_slices()
            slices = id_to_slices[parent_id]
            slices.add_index(index, dashed=dashed)
            if new_parent:
                add_indices_to_parents(nodes, parent_id, id_to_slices, max_missing_edges)

def add_indices_to_parents(nodes, node_id, id_to_slices, max_missing_edges):
    #print('add_indices_to_parents node_id:',node_id)
    type_to_parent_indices = {}
    parent_indices = nodes[node_id].get_parent_indices()
    for parent, indices in parent_indices.items():
        if parent is None:
            continue
        parent_type = parent.get_type()
        parent_id = parent.get_id()
        if (parent_type in type_to_parent_indices and 
            len(type_to_parent_indices[parent_type]) > max_missing_edges): # early stop
            continue
        parent_slices = None
        if parent_id in id_to_slices:
            parent_slices = id_to_slices[parent_id]
        for index in indices:
            if parent_slices is None or not parent_slices.has_index(index):
                if not parent_type in type_to_parent_indices:
                    type_to_parent_indices[parent_type] = []
                parent_indices = type_to_parent_indices[parent_type]
                if len(parent_indices) > max_missing_edges:
                    break
                else:
                    parent_indices.append((parent, index))
    add_parent_indices(nodes, type_to_parent_indices, id_to_slices, max_missing_edges)

def add_missing_edges(nodes, id_to_slices, max_missing_edges=3):
    old_id_to_slices_keys = set(id_to_slices.keys())
    for node_id in old_id_to_slices_keys:
        add_indices_to_parents(nodes, node_id, id_to_slices, max_missing_edges)
    return id_to_slices

# --------------------------------------------------------------------------------------------

import memory_graph.config_helpers as config_helpers

def create_depth_of_nodes(nodes, nodes_at_depth):
    depth_of_nodes = {}
    for node_id, depth in nodes_at_depth.items():
        node = nodes[node_id]
        if node_id in nodes and not node.is_hidden_node():
            if not depth in depth_of_nodes:
                depth_of_nodes[depth] = []
            depth_of_nodes[depth].append(node)
    return depth_of_nodes

def add_subgraph(graphviz_graph, nodes_to_subgraph):
    new_node_names = [node.get_name() for node in nodes_to_subgraph]
    if len(new_node_names) > 1:
        graphviz_graph.body.append('subgraph { rank=same; '+ ' -> '.join(new_node_names) + '[weight='+str(config.graph_stability)+', style=invis]; }\n')

def add_to_graphviz_graph(graphviz_graph, nodes, node, slices, id_to_slices, subgraphed_nodes, depth):
    html_table = node.get_html_table(nodes, slices, id_to_slices)
    edges = html_table.get_edges()
    color = config_helpers.get_color(node)
    border = 3 if node.is_root() else 1
    graphviz_graph.node(node.get_name(),
                        html_table.to_string(border, color),
                        xlabel=node.get_label(slices))
    # ------------ edges
    for parent,child,dashed in edges:
        graphviz_graph.edge(parent, child+':table', style='dashed' if dashed else 'solid')

def build_graph_depth_first(graphviz_graph, nodes,  node_id, id_to_slices, nodes_at_depth, subgraphed_nodes, depth):
    if node_id in id_to_slices:
        if node_id in nodes_at_depth:
            return
        nodes_at_depth[node_id] = depth
        node = nodes[node_id]
        children = node.get_children()
        slices = None
        if node_id in id_to_slices:
            slices = id_to_slices[node_id]
            if not slices is None:
                for index in slices:
                    child_id = id(children[index])
                    build_graph_depth_first(graphviz_graph, nodes, child_id, id_to_slices, nodes_at_depth, subgraphed_nodes, depth+1)
        if not node.is_hidden_node():
            add_to_graphviz_graph(graphviz_graph, nodes, node, slices, id_to_slices, subgraphed_nodes, depth)

def build_graph(graphviz_graph, nodes, root_id, id_to_slices):
    nodes_at_depth = {}
    build_graph_depth_first(graphviz_graph, nodes, root_id, id_to_slices, nodes_at_depth, set(), 0)
    depth_of_nodes = create_depth_of_nodes(nodes, nodes_at_depth)
    #print('nodes_at_depth:',nodes_at_depth,'depth_of_nodes:', depth_of_nodes)
    for depth, depth_nodes in depth_of_nodes.items():
        add_subgraph(graphviz_graph, depth_nodes)

def memory_to_nodes(data):
    nodes, root_id = read_nodes(data)
    #print('nodes:',nodes,'root_id:',root_id)
    id_to_slices = slice_nodes(nodes, root_id, config.max_graph_depth)
    #print('id_to_slices:',id_to_slices)
    id_to_slices = add_missing_edges(nodes, id_to_slices, config.max_missing_edges)
    #print('id_to_slices:',id_to_slices)
    graphviz_graph_attr = {}
    graphviz_node_attr = {'shape':'plaintext'}
    graphviz_edge_attr = {}
    graphviz_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graphviz_graph_attr,
                                    node_attr=graphviz_node_attr,
                                    edge_attr=graphviz_edge_attr)
    build_graph(graphviz_graph, nodes, root_id, id_to_slices)
    return graphviz_graph
