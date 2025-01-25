import memory_graph as mg

image=0
def get_fac_name():
    global image
    image+=1
    return f"debugging{image:02d}.png"

squares = []
squares_collector = []
for i in range(1,6):
    squares.append(i**2)
    squares_collector.append(squares.copy())
    mg.render(locals(), get_fac_name())
mg.d(graph=False,log=True,block=False)