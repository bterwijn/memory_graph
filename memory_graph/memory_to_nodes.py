# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from memory_graph.node_leaf import Node_Leaf
from memory_graph.node_linear import Node_Linear
from memory_graph.node_key_value import Node_Key_Value
import memory_graph.config_helpers as config_helpers

import memory_graph.utils as utils    
import memory_graph.config as config

import graphviz


def read_nodes(data):
    """ Returns 
    - a dictionary that maps the each id found in 'data' to a Node,
    - the ids of node_key_value
    - the id of 'data' as root node.
    """

    def data_to_node(data_type, data):
        """ Returns the Node for 'data' based on it's type. """
        if data_type in config.type_to_node: # for predefined types
            return config.type_to_node[data_type](data)
        elif utils.has_dict_attributes(data): # for user defined classes
            return Node_Key_Value(data, utils.filter_dict(utils.get_dict_attributes(data)) )
        elif utils.is_finite_iterable(data): # for lists, tuples, sets, ...
            return Node_Linear(data, data)
        else:
            return Node_Leaf(data, data)

    def memory_to_nodes_recursive(nodes, nodes_key_value, data, parent, parent_index):
        """ Recursively reads through each reference found in 'data', creates a node for
        it and adds, and adds it to 'nodes'.
        """
        data_type = type(data)
        if not data_type in config.embedded_types or parent is None:
            data_id = id(data)
            if data_id in nodes:
                node = nodes[data_id]
            else:
                node = data_to_node(data_type, data)
                if isinstance(node, Node_Key_Value):
                    nodes_key_value.append(data_id)
                nodes[data_id] = node
                for index in node.get_children().indices_all():
                    child = node.get_children()[index]
                    memory_to_nodes_recursive(nodes, nodes_key_value, child, node, index)
            if not parent is None:
                node.add_parent_index(parent, parent_index)

    nodes = {}
    nodes_key_value = []
    memory_to_nodes_recursive(nodes, nodes_key_value, data, None, None)
    root_id = id(data)
    return nodes, nodes_key_value,root_id


def slice_nodes(nodes, root_id, max_graph_depth):
    """ Returns for nodes in nodes their slices that determines if and what part of
    a node is shown in the graph.
    """

    def get_max_type_depth(node_id, node):
        if node_id in config.type_to_depth:
            return config.type_to_depth[node_id]
        elif node.get_type() in config.type_to_depth:
            return config.type_to_depth[node.get_type()]
        return None
    
    def slice_nodes_recursive(nodes, node_id, id_to_slices, id_to_depth, max_graph_depth):
        """ Recursively start at the root and slice all children until 'max_graph_depth'
        is reached. """
        if max_graph_depth == 0:
            return # ran out of depth
        if node_id in id_to_depth:
            if max_graph_depth <= id_to_depth[node_id]:
                return # already reached with shorter path
        if node_id in nodes:
            node = nodes[node_id]
            children = node.get_children()
            if children.is_empty():
                id_to_slices[node_id] = None
                id_to_depth[node_id] = max_graph_depth
            else:
                if node_id in id_to_slices: # set slices just once, same every time
                    slices = id_to_slices[node_id]
                else:
                    slicer = node.get_slicer()
                    slices = children.slice(slicer)
                    id_to_slices[node_id] = slices
                id_to_depth[node_id] = max_graph_depth
                if not node.is_hidden_node():
                    max_graph_depth -= 1
                max_type_depth = get_max_type_depth(node_id, node)
                if max_type_depth:
                    max_graph_depth = min(max_type_depth, max_graph_depth)
                for index in slices:
                    slice_nodes_recursive(nodes, id(children[index]), id_to_slices, id_to_depth, max_graph_depth)
                    
    id_to_slices = {}
    id_to_depth = {} # more efficient to make these two one dict
    slice_nodes_recursive(nodes, root_id, id_to_slices, id_to_depth, max_graph_depth)
    return id_to_slices


def add_missing_edges(nodes, id_to_slices, max_missing_edges=3):
    """ Add missing edges to each visible node in the graph by addding slices to 'id_to_slices'.
    It either shows all edges to a node, or uses dashed edges to indicate some edges are missing.
    """
    
    def add_parent_indices(nodes, type_to_parent_indices, id_to_slices, max_missing_edges):
        """ Add missing edges in 'type_to_parent_indices' to each parent. If the parent wasn't
        visible before, recursively add missing edges to its parents.
        """ 
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
        """ Go over each parent of 'node_id', and add each missing index to each if it is
        missing. Don't add more than 'max_missing_edges' for each type of parent to keep
        graph small.
        """
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
            parent_slices = id_to_slices.get(parent_id, None)
            for index in indices:
                if parent_slices is None or not parent_slices.has_index(index):
                    type_to_parent_indices.setdefault(parent_type, [])
                    parent_indices = type_to_parent_indices[parent_type]
                    if len(parent_indices) < max_missing_edges:
                        parent_indices.append((parent, index))
        add_parent_indices(nodes, type_to_parent_indices, id_to_slices, max_missing_edges)    
    
    old_id_to_slices_keys = set(id_to_slices.keys())
    for node_id in old_id_to_slices_keys:
        add_indices_to_parents(nodes, node_id, id_to_slices, max_missing_edges)
    return id_to_slices


def embed_keys_in_key_value_nodes(nodes, nodes_key_value, id_to_slices):
    """ Embed keys in Node_Key_Value nodes, so that the keys are not shown as separate nodes. """
    if config.embedded_key_types.issubset(config.embedded_types):
        return # all keys are embedded anyway, nothing to do
    for node_id in nodes_key_value:
        nodekv = nodes[node_id]
        for tuplekv in nodekv.get_children():
            if isinstance(tuplekv,tuple) and len(tuplekv) == 2: # tuple of (key, value)
                key = tuplekv[0]
                if type(key) in config.embedded_key_types:
                    key_id = id(key)
                    if key_id in nodes:
                        node = nodes[key_id]
                        parent_indices = node.get_parent_indices()
                        node_tuplekv = nodes[id(tuplekv)]
                        indices = parent_indices[node_tuplekv]
                        indices.remove(0) 
                        if len(indices) == 0:
                            del parent_indices[node_tuplekv]
                        if len(parent_indices) == 0: # no more parents, remove node
                            del nodes[key_id] # remove the key as node
                            if key_id in id_to_slices:
                                del id_to_slices[key_id]
                                

def build_graph(graphviz_graph, nodes, root_id, id_to_slices):
    """ Builds the graph of 'nodes' in 'graphviz_graph' starting at 'root_id' where 
    'id_to_slices' indicates what is visible in the graph.
    """

    def create_depth_of_nodes(nodes, nodes_at_depth):
        """ Creates a dictionary that maps each depth to the nodes at that depth. """
        depth_of_nodes = {}
        for node_id, depth in nodes_at_depth.items():
            node = nodes[node_id]
            if node_id in nodes and not node.is_hidden_node():
                depth_of_nodes.setdefault(depth, [])
                depth_of_nodes[depth].append(node)
        return depth_of_nodes

    def add_subgraph(graphviz_graph, nodes_to_subgraph):
        """ Adds a subgraph to 'graphviz_graph' for 'nodes_to_subgraph'. """
        new_node_names = [node.get_name() for node in nodes_to_subgraph]
        if len(new_node_names) > 1:
            graphviz_graph.body.append('subgraph { rank=same; '+ ' -> '.join(new_node_names) + '[weight='+str(config.graph_stability)+', style=invis]; }\n')

    def add_to_graphviz_graph(graphviz_graph, nodes, node, slices, id_to_slices, subgraphed_nodes, depth):
        """ Adds 'node' to 'graphviz_graph' with its children and edges. """
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
        """ Recursively builds the graph starting at 'node_id' and adds it to 'graphviz_graph'. """
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

    nodes_at_depth = {}
    build_graph_depth_first(graphviz_graph, nodes, root_id, id_to_slices, nodes_at_depth, set(), 0)
    depth_of_nodes = create_depth_of_nodes(nodes, nodes_at_depth)
    #print('nodes_at_depth:',nodes_at_depth,'depth_of_nodes:', depth_of_nodes)
    for depth, depth_nodes in depth_of_nodes.items():
        add_subgraph(graphviz_graph, depth_nodes)

def memory_to_nodes(data):
    """ Returnd a graph starting at 'data'. """
    nodes, nodes_key_value, root_id = read_nodes(data)
    #print('nodes:',nodes,'root_id:',root_id)
    id_to_slices = slice_nodes(nodes, root_id, config.max_graph_depth)
    #print('id_to_slices:',id_to_slices)
    id_to_slices = add_missing_edges(nodes, id_to_slices, config.max_missing_edges)
    #print('id_to_slices:',id_to_slices)
    embed_keys_in_key_value_nodes(nodes, nodes_key_value, id_to_slices)
    graphviz_graph_attr = {}
    graphviz_node_attr = {'shape':'plaintext'}
    graphviz_edge_attr = {}
    graphviz_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graphviz_graph_attr,
                                    node_attr=graphviz_node_attr,
                                    edge_attr=graphviz_edge_attr)
    build_graph(graphviz_graph, nodes, root_id, id_to_slices)
    return graphviz_graph
