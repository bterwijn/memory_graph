import memory_graph
memory_graph.config.not_node_types.remove(int) # show references to ints

a = 10
b = a
memory_graph.render(locals(), 'immutable1.png')
a += 1
memory_graph.render(locals(), 'immutable2.png')
