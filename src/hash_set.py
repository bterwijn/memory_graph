import random

class Hash_Set:
    
        def __init__(self, capacity):
            self.buckets = [None] * capacity
    
        def add(self, value):
            index = hash(value) % len(self.buckets)
            if self.buckets[index] is None:
                self.buckets[index] = []
            if not value in self.buckets[index]:
                bucket = self.buckets[index]
                bucket.append(value)
        
        def contains(self, value):
            index = hash(value) % len(self.buckets)
            if self.buckets[index] is None:
                return False
            return value in self.buckets[index]
        
        def remove(self, value):
            index = hash(value) % len(self.buckets)
            if self.buckets[index] is not None:
                self.buckets[index].remove(value)
        
hash_set = Hash_Set(10)
n = 15
max_rand_value = int(n * 1.5)
values = [random.randrange(max_rand_value) for _ in range(n)]

print('adding values: ', values)
for value in values:
    hash_set.add(value)

random.shuffle(values)
print('removing values: ', values)
for value in values:
    if hash_set.contains(value):
        hash_set.remove(value)
