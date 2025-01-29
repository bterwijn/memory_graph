# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import numpy as np
import memory_graph.extension_numpy
np.random.seed(0) # use same random numbers each run

array = np.array([1.1, 2, 3, 4, 5])
matrix = np.matrix([[i*20+j for j in range(20)] for i in range(20)])
ndarray = np.random.rand(20,20)

mg.render( locals(), "extension_numpy.png")
