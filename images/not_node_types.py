import memory_graph as mg

a = [100, 200, 300]
b = a.copy()
mg.render(locals(), 'not_node_types1.png')

mg.config.not_node_types.remove(int) # create a node for int values

mg.render(locals(), 'not_node_types2.png')
