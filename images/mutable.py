import memory_graph

a = [4, 3, 2]
b = a
memory_graph.render(locals(), 'mutable1.png')
a += [1] # equivalent to:  a.append(1)
memory_graph.render(locals(), 'mutable2.png')
