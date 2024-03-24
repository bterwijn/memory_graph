import numpy as np
import config
from Node_Linear import Node_Linear
from Node_Table import Node_Table

config.no_reference_types |= {
    np.int8 : lambda d : str(d), 
    np.int16 : lambda d : str(d), 
    np.int32 : lambda d : str(d), 
    np.int64 : lambda d : str(d),
    np.uint8 : lambda d : str(d), 
    np.uint16 : lambda d : str(d), 
    np.uint32 : lambda d : str(d), 
    np.uint64 : lambda d : str(d),
    np.float16 : lambda d : str(d), 
    np.float32 : lambda d : str(d), 
    np.float64 : lambda d : str(d), 
    np.float_ : lambda d : str(d),
    np.complex64 : lambda d : str(d), 
    np.complex128 : lambda d : str(d), 
    np.complex_ : lambda d : str(d),
    np.bool_ : lambda d : str(d), 
    np.bytes_ : lambda d : str(d), 
    np.str_ : lambda d : str(d),
    np.datetime64 : lambda d : str(d), 
    np.timedelta64 : lambda d : str(d), 
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
