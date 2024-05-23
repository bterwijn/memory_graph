import memory_graph


d =  {1:100, 2:200}
data = [[i for i in range(20)], [100,200], d]

memory_graph.show(data)
