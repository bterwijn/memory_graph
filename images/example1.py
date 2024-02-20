import memory_graph

data = [ (1, 2), [3, 4], {5, 6}, {7:'seven', 8:'eight'} ]
memory_graph.render( data ,'example1.png', block=False)
