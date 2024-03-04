import memory_graph
import copy

class My_Class:

    def __init__(self):
        self.digits = [1, 2]
        self.letters = ['x', 'y']

    def copy(self): # custom copy method copies the digits but shares the letters
        c = copy.copy(self)
        c.digits = copy.copy(self.digits)
        return c

a = My_Class()
b = a.copy()

memory_graph.render(locals(), 'copy_method.png')
