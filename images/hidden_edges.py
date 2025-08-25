import memory_graph as mg

data = []
x = ['x']
for i in range(20):
    data.append(x)

mg.render(locals(), 'hidden_edges.png')
