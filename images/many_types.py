# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

class My_Class:
    def __init__(self, x, y):
        self.x = x
        self.y = y

data = [ range(1, 2), (3, 4), {5, 6}, {7:'seven', 8:'eight'},  My_Class(9, 10) ]
mg.render(data, 'many_types.png')
