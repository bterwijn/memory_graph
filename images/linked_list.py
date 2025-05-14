# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import random
random.seed(0) # use same random numbers each run

class Linked_List:

    def __init__(self, value=None, prev=None, next=None):
        self.prev = prev
        self.value = value
        self.next = next

    def add_front(self, value):
        if self.value == None:
            self.value = value 
        elif self.next is None:
            new_node = Linked_List(value)
            self.prev = new_node
            self.next = new_node
        else:
            new_node = Linked_List(value, self.next)
            self.next.next = new_node
            self.next = new_node

linked_list = Linked_List()
n = 100
for i in range(n):
    value = random.randrange(n)
    linked_list.add_front(value)
    if value == 33:
        mg.render(locals(), "linked_list.png")
        exit()
