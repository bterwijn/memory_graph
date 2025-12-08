import memory_graph as mg
import random

class Hash_Map:

    def __init__(self, size=25):
        self.buckets = [[] for i in range(size)]

    def _get_bucket(self, key):
        index = hash(key) % len(self.buckets)
        return self.buckets[index]

    def __setitem__(self, key, value):
        bucket = self._get_bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def __getitem__(self, key):
        bucket = self._get_bucket(key)
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

hash_map = Hash_Map()
n = 20
value_range = n * 3 
for i in range(n):
    key = random.randint(1, value_range)
    hash_map[f"key_{key}"] = f"value_{key}"

for i in range(n):
    key = random.randint(1, value_range)
    try:
        value = hash_map[f"key_{key}"]
        print(f"Retrieved: key_{key} -> {value}")
    except KeyError:
        print(f"key_{key} not found in hash map")    


