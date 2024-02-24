import memory_graph

def add_one(a, b, c):
    a += 1
    b.append(1)
    c.append(1)
    memory_graph.render( memory_graph.get_call_stack(), "add_one.png")

a = 0
b = [4, 3, 2]
c = [4, 3, 2]

add_one(a,b,c.copy())
print(f"a:{a} b:{b} c:{c}")
