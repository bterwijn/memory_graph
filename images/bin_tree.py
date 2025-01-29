# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import random
random.seed(0) # use same random numbers each run

class Node:

    def __init__(self, value):
        self.smaller = None
        self.value = value
        self.larger = None

class BinTree:

    def __init__(self):
        self.root = None

    def add_recursive(self, new_value, node):
        if new_value < node.value:
            if node.smaller is None:
                node.smaller = Node(new_value)
            else:
                self.add_recursive(new_value, node.smaller)
        else:
            if node.larger is None:
                node.larger = Node(new_value)
            else:
                self.add_recursive(new_value, node.larger)
        if new_value == 51:
            mg.render(locals(), f"bin_tree.png")
            exit(0)

    def add(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.add_recursive(value, self.root)

tree = BinTree()
n = 100
for i in range(n):
    new_value = random.randrange(n)
    tree.add(new_value)

