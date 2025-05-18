# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import random
random.seed(0) # use same random numbers each run

class Linked_List:
    """ Circular doubly linked list """

    def __init__(self, value=None, 
                 prev=None, next=None):
        self.prev = prev if prev else self
        self.value = value
        self.next = next if next else self

    def add_back(self, value):
        if self.value == None:
            self.value = value 
        else:
            new_node = Linked_List(value,
                                   prev=self.prev,
                                   next=self)
            self.prev.next = new_node
            self.prev = new_node

linked_list = Linked_List()
n = 100
for i in range(n):
    value = random.randrange(n)
    linked_list.add_back(value)
    if value == 33:
        mg.render(locals(), "linked_list.png")
        exit()
