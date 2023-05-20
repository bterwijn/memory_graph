import memory_graph

data = [ (1, 2), [3, 4], {5:'five', 6:'six'} ]
memory_graph.render( data ,'example1.png', block=False)
