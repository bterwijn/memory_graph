import memory_graph
import random
random.seed(0) # use same random numbers each run

class HashSet:
    
        def __init__(self, capacity=20):
            self.capacity = capacity
            self.buckets = [None] * capacity
    
        def add(self, value):
            index = hash(value) % self.capacity
            if self.buckets[index] is None:
                self.buckets[index] = [value]
            else:
                self.buckets[index].append(value)

        def contains(self, value):
            index = hash(value) % self.capacity
            if self.buckets[index] is None:
                return False
            return value in self.buckets[index]
        
hash_set = HashSet()
n = 100
for i in range(n):
    new_value = random.randrange(n)
    hash_set.add(new_value)
    if new_value == 36:
        memory_graph.render(locals(), "hash_set.png")
        exit()
