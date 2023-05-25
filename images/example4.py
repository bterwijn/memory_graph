import pandas as pd

data = {'Name':['Tom', 'Anna', 'Steve', 'Lisa'],
        'Age':[28,34,29,42],
        'Length':[1.70,1.66,1.82,1.73] }
df = pd.DataFrame(data)

import memory_graph
memory_graph.rewrite.custom_accessor_functions[pd.DataFrame] = lambda d: list(d.iteritems())
memory_graph.rewrite.custom_accessor_functions[pd.Series] = lambda d: list(d.items())
memory_graph.rewrite_to_node.reduce_reference_parents.add("DataFrame")
memory_graph.rewrite_to_node.reduce_reference_parents.add("Series")
memory_graph.graphviz_nodes.category_to_color_map['Series'] = 'lightskyblue'
memory_graph.render( locals(), 'example4.png' )
