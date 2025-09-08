import copy

class My_Class:

    def __init__(self):
        self.digits = [1, 2]
        self.letters = ['x', 'y']

    def custom_copy(self): 
        """ Copies 'digits' but shares 'letters'. """
        c = copy.copy(self)
        c.digits = copy.copy(self.digits)
        return c

a = My_Class()
b = a.custom_copy()
