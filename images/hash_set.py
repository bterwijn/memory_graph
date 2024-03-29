import memory_graph
import random
random.seed(0) # use same random numbers each run

class HashSet:
    
        def __init__(self, capacity=20):
            self.buckets = [None] * capacity
    
        def add(self, value):
            index = hash(value) % len(self.buckets)
            if self.buckets[index] is None:
                self.buckets[index] = []
            bucket = self.buckets[index]
            bucket.append(value)
            if value == 36:
                memory_graph.render(locals(), "hash_set.png")
                exit()
        
        def contains(self, value):
            index = hash(value) % len(self.buckets)
            if self.buckets[index] is None:
                return False
            return value in self.buckets[index]
        
        def remove(self, value):
            index = hash(value) % len(self.buckets)
            if self.buckets[index] is not None:
                self.buckets[index].remove(value)
        
hash_set = HashSet()
n = 100
for i in range(n):
    new_value = random.randrange(n)
    hash_set.add(new_value)
