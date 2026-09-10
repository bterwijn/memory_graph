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

    def print_values(self):
        if self.smaller:
            self.smaller.print_values()
        print(self.value, end=' ')
        if self.larger:
            self.larger.print_values()

tree = Bin_Tree()
print("build the tree")
n = 20
for i in range(n):
    value = random.randint(0, n * 10)
    print(f'{i+1}/{n} insert: {value}')
    tree.add(value)

print("print values in sorted order")
tree.print_values()
