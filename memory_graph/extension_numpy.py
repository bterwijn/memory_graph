# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Extension to add the memory graph configuration for Numpy types. """
from memory_graph.node_linear import Node_Linear
from memory_graph.node_table import Node_Table

import memory_graph.config as config

import numpy as np

config.embedded_types |= {
    np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64, 
    np.float16, np.float32, np.float64,
    np.complex64, np.complex128,
    np.bool_, np.bytes_, np.str_, np.datetime64, np.timedelta64
}

def ndarray_to_node(data, ndarray_data):
    dim = len(ndarray_data.shape)
    if dim > 2:
        return Node_Linear(data, [i for i in ndarray_data])
    elif dim == 2:
        return Node_Table(data, ndarray_data)
    else:
        return Node_Linear(data, ndarray_data)

config.type_to_node[np.matrix] = lambda data : Node_Table(data, np.asarray(data)) # convert to ndarray to avoid infinite recursion due to index issue
config.type_to_node[np.ndarray] = lambda data : ndarray_to_node(data, data)

config.type_to_color[np.ndarray] = "hotpink1"
config.type_to_color[np.matrix] = "hotpink2"
