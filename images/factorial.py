import memory_graph

image=0
def get_fac_name():
    global image
    image+=1
    return f"factorial{image:02d}.png"

def factorial(n):
    if n==0:
        return 1
    #memory_graph.show( memory_graph.get_call_stack(), block=True ) # draw graph
    memory_graph.render( memory_graph.get_call_stack(), get_fac_name())
    result = n*factorial(n-1)
    #memory_graph.show( memory_graph.get_call_stack(), block=True ) # draw graph
    memory_graph.render( memory_graph.get_call_stack(), get_fac_name())
    return result

memory_graph.render( memory_graph.get_call_stack(), get_fac_name())
factorial(3)