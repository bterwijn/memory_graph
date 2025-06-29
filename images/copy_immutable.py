# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import copy

a = ( (1, 2), ('x', 'y') ) # a nested tuple

# three different ways to make a "copy" of 'a':
c1 = a
c2 = copy.copy(a)
c3 = copy.deepcopy(a)

mg.render(locals(), 'copy_immutable.png')
