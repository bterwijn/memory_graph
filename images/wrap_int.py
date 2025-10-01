# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

def add_one(a, b):
    a += 1
    b[0] += 1
    mg.render( mg.stack(), "wrap_int.png")

a = 10
b = [10]

add_one(a, b)
print(f"a:{a} b:{b[0]}")
