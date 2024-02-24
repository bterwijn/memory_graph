import memory_graph
import copy

class My_Class:

    def __init__(self):
        self.numbers = [1, 2]
        self.letters = ['x', 'y']

    def copy(self): # custom copy method copies the numbers but shares the letters
        c = copy.copy(self)
        c.numbers = copy.copy(self.numbers)
        return c

a = My_Class()
b = a.copy()

memory_graph.render(locals(), 'copy_method.png')
