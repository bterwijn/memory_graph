import random

mg.config.type_to_horizontal[list] = True # Visualize lists horizontally

class Multi_Tree:
    max_children = 4

    def __init__(self):
        self.values = []
        self.children = []

    def add_value(self, value):
        if len(self.values) < self.max_children - 1:
            self.values.append(value)
            self.values.sort()
        else:
            if not self.children:
                for _ in range(self.max_children):
                    self.children.append(Multi_Tree())
            index = self._find_child_index(value)
            self.children[index].add_value(value)

    def _find_child_index(self, value):
        for i, v in enumerate(self.values):
            if value < v:
                return i
        return len(self.values)  # last child

tree = Multi_Tree()
n = 50
for i in range(n):
    tree.add_value(random.randint(1, n * 10))
