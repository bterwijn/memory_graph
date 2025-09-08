import numpy as np
import memory_graph.extension_numpy

matrix = np.matrix([[i*5+j for j in range(4)] for i in range(5)])
ndarray_1d = np.array([1.1, 2, 3, 4, 5])
ndarray_2d = np.random.rand(3,2)
ndarray_3d = np.random.rand(2,2,2)
