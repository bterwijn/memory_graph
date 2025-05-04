# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import bintrees

# Create an AVL tree
tree = bintrees.AVLTree()
tree.insert(10, "ten")
tree.insert(5, "five")
tree.insert(20, "twenty")
tree.insert(15, "fifteen")

# mg.render(locals(), 'avltree_fail.png') # id keeps changing

mg.config.type_to_color[bintrees.avltree.Node] = "sandybrown"
mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_linear.Node_Linear(data, dir(data))
mg.config.type_to_slicer[bintrees.avltree.Node] = mg.slicer.Slicer()
mg.render(locals(), 'avltree_dir.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_leaf.Node_Leaf(data, f"key:{data.key} value:{data.value}")
mg.render(locals(), 'avltree_leaf.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_linear.Node_Linear(data,
                                                                                        ['left:', data.left,
                                                                                         'key:', data.key,
                                                                                         'value:', data.value,
                                                                                         'right:', data.right])
mg.render(locals(), 'avltree_linear.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_key_value.Node_Key_Value(data,
                                                                                              {'left': data.left,
                                                                                               'key': data.key,
                                                                                               'value': data.value,
                                                                                               'right': data.right}.items())
mg.render(locals(), 'avltree_key_value.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_table.Node_Table(data,
                                                                                      [[data.key, data.value],
                                                                                       [data.left, data.right]]
                                                                                      )
mg.render(locals(), 'avltree_table.png')
