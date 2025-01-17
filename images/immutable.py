import memory_graph

a = (4, 3, 2)
b = a
memory_graph.render(locals(), 'immutable1.png')
a += (1,)
memory_graph.render(locals(), 'immutable2.png')
