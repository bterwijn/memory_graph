# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause


import memory_graph.memory_to_nodes as memory_to_nodes
import memory_graph.config_helpers as config_helper

config_helper.set_config()

l1 = [1,2]
l2 = [3,4]
data = [l1,l2,l1,[5,l2]]
nodes = memory_to_nodes.memory_to_nodes(data)
#print(nodes)