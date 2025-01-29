# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
from memory_graph.slicer import Slicer

data = [ list(range(20)) for i in range(1,5)]
highlight = data[2]

mg.render( locals(), "highlight.png",
    colors                = {id(highlight): "red"   }, # set color to "red"
    vertical_orientations = {id(highlight): False   }, # set horizontal orientation
    slicers               = {id(highlight): Slicer()}  # set no slicing
)
