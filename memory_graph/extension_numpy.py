""" Extension to add the memory graph configuration for Numpy types. """
from memory_graph.Node_Linear import Node_Linear
from memory_graph.Node_Table import Node_Table

import memory_graph.config as config

import numpy as np

config.no_reference_types |= {
    np.int8 : lambda d : d, 
    np.int16 : lambda d : d, 
    np.int32 : lambda d : d, 
    np.int64 : lambda d : d,
    np.uint8 : lambda d : d, 
    np.uint16 : lambda d : d, 
    np.uint32 : lambda d : d, 
    np.uint64 : lambda d : d,
    np.float16 : lambda d : d, 
    np.float32 : lambda d : d, 
    np.float64 : lambda d : d, 
    np.float_ : lambda d : d,
    np.complex64 : lambda d : d, 
    np.complex128 : lambda d : d, 
    np.complex_ : lambda d : d,
    np.bool_ : lambda d : d, 
    np.bytes_ : lambda d : d, 
    np.str_ : lambda d : d,
    np.datetime64 : lambda d : d, 
    np.timedelta64 : lambda d : d, 
}

def ndarray_to_node(ndarray_data):
    if len(ndarray_data.shape) == 2:
        return Node_Table(ndarray_data, ndarray_data)
    else:
        return Node_Linear(ndarray_data, ndarray_data)
    
config.type_to_node[np.matrix] = lambda data : (
    Node_Table(data, data.getA1(), data.shape[1])
            )
config.type_to_node[np.ndarray] = ndarray_to_node

config.type_to_color[np.ndarray] = "hotpink1"
config.type_to_color[np.matrix] = "hotpink2"
