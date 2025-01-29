# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import random
random.seed(0) # use same random numbers each run

class Node:

    def __init__(self, value):
        self.prev = None
        self.value = value
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def add_front(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

linked_list = LinkedList()
n = 100
for i in range(n):
    new_value = random.randrange(n)
    linked_list.add_front(new_value)
    if new_value == 33:
        mg.render(locals(), "linked_list.png")
        exit()
