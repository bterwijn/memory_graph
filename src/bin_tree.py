import random

class Bin_Tree:

    def __init__(self, value=None):
        self.smaller = None
        self.value = value
        self.larger = None

    def add(self, value):
        if self.value is None:
            self.value = value
        elif value < self.value:
            if self.smaller is None:
                self.smaller = Bin_Tree(value)
            else:
                self.smaller.add(value)
        else:
            if self.larger is None:
                self.larger = Bin_Tree(value)
            else:
                self.larger.add(value)

tree = Bin_Tree()
n = 20
for i in range(n):
    tree.add(random.randint(0,100))
