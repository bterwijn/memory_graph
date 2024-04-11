import memory_graph

my_squares = []
my_squares_ref = my_squares
for i in range(5):
    my_squares.append(i**2)
my_squares_copy = my_squares.copy()
memory_graph.render(locals(), 'debugging.png')
