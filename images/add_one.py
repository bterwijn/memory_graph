# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

def add_one(a, b, c):
    a += [1]
    b += (1,)
    c += [1]
    mg.render( mg.stack(), "add_one.png")

a = [4, 3, 2]
b = (4, 3, 2)
c = [4, 3, 2]

add_one(a, b, c.copy())
print(f"a:{a} b:{b} c:{c}")
