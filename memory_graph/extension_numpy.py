""" Extension to add the memory graph configuration for Numpy types. """
from memory_graph.element_linear import Element_Linear
from memory_graph.element_table import Element_Table

import memory_graph.config as config

import numpy as np

config.no_reference_types |= {
    np.int8, np.int16, np.int32, np.int64, np.uint8, np.uint16, np.uint32, np.uint64, 
    np.float16, np.float32, np.float64, np.float_, 
    np.complex64, np.complex128, np.complex_, 
    np.bool_, np.bytes_, np.str_, np.datetime64, np.timedelta64
}

def ndarrayy_to_node(ndarrayy_data):
    if len(ndarrayy_data.shape) == 2:
        return Element_Table(ndarrayy_data, ndarrayy_data.tolist()) # convert to list for stable id(element)
    else:
        return Element_Linear(ndarrayy_data, ndarrayy_data.tolist()) # convert to list for stable id(element)
    
config.type_to_element[np.matrix] = lambda data : Element_Table(data, data.tolist()) # convert to list for stable id(element) 
config.type_to_element[np.ndarray] = lambda data :  ndarrayy_to_node(data)

config.type_to_color[np.ndarray] = "hotpink1"
config.type_to_color[np.matrix] = "hotpink2"
