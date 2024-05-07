import memory_graph.memory_to_elements as memory_to_elements
import memory_graph.print_elements as print_elements
import memory_graph.slice_elements as slice_elements

import memory_graph.config_default
import memory_graph.config_helpers as config_helpers

config_helpers.set_config()

a = list(range(20))
b = set(range(10))
a.append(b)
data = [a, b]

root_element = memory_to_elements.to_elements(data) 
print('root_element:', root_element)
print_elements.print_elements(root_element)

sliced_elements = slice_elements.slice_elements(root_element)
for key,value in sliced_elements.items():
    print(f'{key}: {value}')
