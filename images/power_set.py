# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

image = 1

def get_subsets(subsets, data, i, subset):
    global image
    mg.render(mg.stack(), f"power_set{image}.png")
    image += 1
    if i == len(data):
        subsets.append(subset.copy())
        return
    subset.append(data[i])
    get_subsets(subsets, data, i+1, subset) #    do include data[i]
    subset.pop()
    get_subsets(subsets, data, i+1, subset) # don't include data[i]
    mg.render(mg.stack(), f"power_set{image}.png")
    image += 1

def power_set(data):
    subsets = []
    get_subsets(subsets, data, 0, [])
    return subsets

print( power_set(['a', 'b', 'c']) )
