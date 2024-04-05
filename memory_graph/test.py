""" Some test data to make memory graph of for test purposes. """
import memory_graph.utils as utils
import memory_graph.config as config

import numpy as np
import pandas as pd
import memory_graph.extension_numpy
import memory_graph.extension_pandas

from memory_graph.Node_Table import Node_Table
from memory_graph.Memory_Graph import Memory_Graph

def test_singular(fun):
    data = 100
    fun(data)

def test_linear(fun):
    data = [None, True, 1, 2.2, complex(3,4), 'hello this is a very long string that should be cut off at some point.']
    fun(data)

def test_linears(fun):
    data = [(1,2), [3,4], {5,6}, frozenset((7,8)), {9:'nine', 10:'ten'} , bytes('11', 'utf-8'), bytearray('12', 'utf-8')]
    data.append( [i for i in range(20)] )
    fun(data)

def test_colors(fun):
    data1 = [None, True, 1, 2.2, complex(3,4), 'hello']
    class My_Class:
        class_var = 1
        def __init__(self):
            self.var=2
    data2 = [(1,2), [3,4], {5,6}, frozenset((7,8)), {9:'9', 10:'10'} , bytes('11', 'utf-8'), bytearray('12', 'utf-8'), My_Class(), My_Class]
    restore = config.no_reference_types.copy()
    config.no_reference_types.clear()
    fun([data1, data2])
    config.no_reference_types = restore

def test_empty_linear(fun):
    data = [tuple(), list(), set(), frozenset(), dict() , bytes(), bytearray()]
    fun(data)

def test_nested_list(fun):
    data = utils.nested_list([2,3,4,5])
    fun(data)

def test_key_value(fun):
    data1 = {1:'a', 2:'b', 3:'c', 4:'d'}
    data2 = {10:100, 20:200, 30:300, 40:400}
    data2[50] = ('c','c')
    data2[60] = data1
    data = {'first':data1, 'second':data2}
    fun(data)

def test_class(fun):
    class My_Class1:
        def __init__(self):
            self.foo1=10
            self.bar1=20
    class My_Class2:
        def __init__(self):
            self.foo2=10
            self.bar2=20
    data = [My_Class1(), My_Class2()]
    fun(data)

def test_class_vars(fun):
    class My_Class1:
        class_var1 = 'a'
        class_var2 = 'b'
        def __init__(self):
            self.var1=10
            self.var2=20
        def my_method(self):
            return 100
    data = [My_Class1, My_Class1()]
    fun(data)

def test_share_tuple(fun):
    class My_Class:
        def __init__(self):
            self.a=1
    data = [('a',1), ('a',1), {'a':1}, {'a':1}, My_Class(),My_Class()]
    fun(data)

def test_share_children(fun):
    a=['a']
    b=['b']
    c=['c']
    d=['d']
    data = [ [a,b,c,], [a,c,d] ]
    fun(data)

def test_list_split(fun):
    data = [ list(range(i)) for i in range(50) ]
    fun(data)

def test_key_value_split(fun):
    data = { i:i*10 for i in range(1,20)}
    fun(data)

def test_table(fun):
    class My_Table:
        def __init__(self,size):
            self.size=size
            self.data = [i for i in range(size[0]*size[1])]
    data = My_Table((10,10))
    config.type_to_color[My_Table] = 'plum1'
    config.type_to_node[My_Table] = lambda data: (
            Node_Table(data, data.data , data.size[0], 
                        #column_names = [f'col{i}' for i in range(data.size[1])],
                        #row_names = [f'row{i}' for i in range(data.size[0])] 
            )
    )
    fun(data)

def test_numpy(fun):
    data = [np.array([1.1, 2, 3, 4, 5]), 
            np.matrix([[i*20+j for j in range(20)] for i in range(20)]), 
            np.random.rand(20,20)]
    #data = np.matrix('1 2; 3 4')
    fun(data)

def test_pandas(fun):
    data = [
            pd.DataFrame({  "calories": [420, 380, 390],
                            "duration": [50, 40, 45]
                        }),

            pd.DataFrame({  'Name'   : [ 'Tom', 'Anna', 'Steve', 'Lisa'],
                            'Age'    : [    28,     34,      29,     42],
                            'Length' : [  1.70,   1.66,    1.82,   1.73] },
                            index=['one', 'two', 'three', 'four']),

            pd.Series( [i for i in range(20)] )
            ]
    fun(data)

def example_function(a):
    return a*10

class Example_Class:

    def __init__(self):
        self.a=1
        self.b=2
    def example_method(self):
        return self.a+self.b

def test_function(fun):
    data = [1,2,example_function,lambda x: x*100, Example_Class, Example_Class.example_method]
    fun(data)

def test_memory_graph(fun):
    data = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
    graph = Memory_Graph(data)
    data.append(graph)
    fun(data)

def test_all(fun):
    pass
    test_singular(fun)
    test_linear(fun)
    test_linears(fun)
    test_colors(fun)
    test_empty_linear(fun)
    test_nested_list(fun)
    test_key_value(fun)
    test_class(fun)
    test_class_vars(fun)
    test_share_tuple(fun)
    test_share_children(fun)
    test_list_split(fun)
    test_key_value_split(fun)
    test_table(fun)
    test_numpy(fun)
    test_pandas(fun)
    test_function(fun)
    test_memory_graph(fun)