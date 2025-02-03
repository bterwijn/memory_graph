# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

def build_nested_list(depth = 15):
    first = [1,2]
    last = first
    if depth>0:
        first2, last = build_nested_list(depth-1)
        first.append(first2)
    return first, last

first,last = build_nested_list(15)
for i in range(20):
    last.append('X')

child = ('who', 'are', 'my', 'parents?')
last[4] = child
last[5] = child
last[6] = child
last[7] = child
last[8] = child

mg.show([first,child])
#mg.show([first])