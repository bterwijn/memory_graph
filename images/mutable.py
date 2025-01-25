import memory_graph as mg

a = [4, 3, 2]
b = a
mg.render(locals(), 'mutable1.png')
a += [1] # equivalent to:  a.append(1)
mg.render(locals(), 'mutable2.png')
