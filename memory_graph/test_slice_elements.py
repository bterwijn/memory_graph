import memory_graph.memory_to_elements as memory_to_elements
import memory_graph.print_elements as print_elements
import memory_graph.slice_elements as slice_elements
import memory_graph.add_missing_edges as add_missing_edges

import memory_graph.config_default
import memory_graph.config_helpers as config_helpers

config_helpers.set_config()

a = [1,2]
b = [3,4,a]
c = [5,6,b]
long_list = list(range(30))
long_list[7]=c
data = [long_list, a]

print('=== memory_to_elements')
root_element = memory_to_elements.to_elements(data) 
print('root_element:', root_element)
print_elements.print_elements(root_element)

print('=== slice_elements')
sliced_elements = slice_elements.slice_elements(root_element, 10)
for key,value in sliced_elements.items():
    print(f'{key}: {value}')

print('=== add_missing_edges')
sliced_elements = add_missing_edges.add_missing_edges(sliced_elements)
for key,value in sliced_elements.items():
    print(f'{key}: {value}')