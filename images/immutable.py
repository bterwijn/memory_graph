# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

a = (4, 3, 2)
b = a
mg.render(locals(), 'immutable1.png')
a += (1,)
mg.render(locals(), 'immutable2.png')
