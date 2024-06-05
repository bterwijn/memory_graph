import memory_graph.memory_to_elements as memory_to_elements
import memory_graph.print_elements as print_elements
import memory_graph.slice_elements as slice_elements
import memory_graph.add_missing_edges as add_missing_edges
import memory_graph.build_graph as build_graph

import memory_graph.config_default
import memory_graph.config_helpers as config_helpers

import graphviz

import numpy as np
import memory_graph.extension_numpy
import pandas as pd
import memory_graph.extension_pandas

config_helpers.set_config()

a = [1,2]
b = [3,4,a]
c = [5,6,b]
long_list = list(range(30))
long_list[7]=c
dic = {i:i*100 for i in range(20)}
matrix = np.random.rand(15,8)
table = pd.DataFrame({  'Name'   : [ 'Tom', 'Anna', 'Steve', 'Lisa'],
                        'Age'    : [    28,     34,      29,     42],
                        'Length' : [  1.70,   1.66,    1.82,   1.73] },
                        index=['one', 'two', 'three', 'four'])

data = [long_list, a, dic, matrix, table]


#data = [dic]

#print('=== memory_to_elements')
root_element = memory_to_elements.to_elements(data) 
#print('root_element:', root_element)
#print_elements.print_elements(root_element)

#print('=== slice_elements')
sliced_elements = slice_elements.slice_elements(root_element, 10)
#for key,value in sliced_elements.items():
#    print(f'{key}: {value}')

#print('=== add_missing_edges')
sliced_elements = add_missing_edges.add_missing_edges(sliced_elements)
#for key,value in sliced_elements.items():
#    print(f'{key}: {value}')

#print('=== create graphviz_graph')
graphviz_graph_attr = {}
graphviz_node_attr = {'shape':'plaintext'}
graphviz_edge_attr = {}
graphviz_graph=graphviz.Digraph('memory_graph',
                                graph_attr=graphviz_graph_attr,
                                node_attr=graphviz_node_attr,
                                edge_attr=graphviz_edge_attr)

#print('=== build_graph')
build_graph.build_graph(graphviz_graph, root_element, sliced_elements)
graphviz_graph.render(outfile="test.png")