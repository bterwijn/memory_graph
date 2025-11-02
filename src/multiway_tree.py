import random

mg.config.type_to_horizontal[list] = True  # show lists horizontally

class Multiway_Tree:
    max_children = 4

    def __init__(self):
        self.values = []
        self.children = []

    def _find_child_index(self, value):
        for i, v in enumerate(self.values):
            if value < v:
                return i
        return len(self.values)  # last child

    def add_value(self, value):
        if len(self.values) < self.max_children - 1:
            self.values.append(value)
            self.values.sort()
        else:
            if not self.children:
                self.children = [None] * self.max_children
            index = self._find_child_index(value)
            if self.children[index] is None:
                self.children[index] = Multiway_Tree()
            self.children[index].add_value(value)

tree = Multiway_Tree()
n = 50
for i in range(n):
    tree.add_value(random.randint(1, n * 10))
