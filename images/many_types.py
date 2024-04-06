import memory_graph

class MyClass:
    def __init__(self, x, y):
        self.x = x
        self.y = y

data = [ range(1, 2), (3, 4), {5, 6}, {7:'seven', 8:'eight'},  MyClass(9, 10) ]
memory_graph.render( data ,'example1.png')
