import memory_graph

class test_class:
    class_var = 100

    def __init__(self) -> None:
        self.instance_var = 200

a = 10
b = 100
c = 1000

print(locals())

memory_graph.show( locals() )
