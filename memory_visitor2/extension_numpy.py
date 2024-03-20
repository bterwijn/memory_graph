import numpy as np
import config
from Node_Linear import Node_Linear
from Node_Table import Node_Table

config.no_reference_types |= {
    np.int8, np.int16, np.int32, np.int64,
    np.uint8, np.uint16, np.uint32, np.uint64,
    np.float16, np.float32, np.float64, np.float_,
    np.complex64, np.complex128, np.complex_,
    np.bool_, np.bytes_, np.str_,
    np.datetime64, np.timedelta64
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
