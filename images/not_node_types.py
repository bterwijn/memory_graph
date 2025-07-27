import memory_graph as mg

a = [100, 200, 300]
b = a.copy()
mg.render(locals(), 'embedded1.png')

mg.config.embedded_types.remove(int) # create a node for int values

mg.render(locals(), 'embedded2.png')
