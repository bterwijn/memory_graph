import memory_graph as mg
import traceback;

def fun3():
    d = [0] * 3
    for i in range(4):
        d[i] = i  # throws IndexError when i = 3
    
def fun2():
    fun3()
    
def fun1():
    fun2()

try:
    fun1()
except Exception as e:
    traceback.print_exc()           # print trace back
    mg.render(mg.stack_exception(e), 'exception_example.png')  # graph trace back
