# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

def factorial(n):
    mg.render( mg.stack(), 'factorial.png', numbered=True)
    if n==0:
        return 1
    result = n*factorial(n-1)
    mg.render( mg.stack(), 'factorial.png', numbered=True)
    return result

mg.render( mg.stack(), 'factorial.png', numbered=True)
factorial(4)
