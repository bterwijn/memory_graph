# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

def factorial(n):
    if n==0:
        return 1
    mg.render( mg.stack(), 'factorial.png', count_file=True)
    result = n*factorial(n-1)
    mg.render( mg.stack(), 'factorial.png', count_file=True)
    return result

mg.render( mg.stack(), 'factorial.png', count_file=True)
factorial(3)
