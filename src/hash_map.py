import random

class Hash_Map:
    INITIAL_SIZE = 5
    REHASH_RATIO = 1.5

    def __init__(self, size=None):
        if not size:
            size = Hash_Map.INITIAL_SIZE
        self.buckets = [[] for i in range(size)]
        self.key_count = 0

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
        self.key_count += 1
        ratio = self.key_count / len(self.buckets)
        if ratio > Hash_Map.REHASH_RATIO:
            self.rehash()

    def __getitem__(self, key):
        bucket = self._get_bucket(key)
        for k, v in bucket:
            if k == key:
                return v
        raise KeyError(f"Key {key} not found")

    def __delitem__(self, key):
        bucket = self._get_bucket(key)
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return
        raise KeyError(f"Key {key} not found")

    def rehash(self):
        print("rehashing...")
        new_size = len(self.buckets) * 2  # double size
        new_buckets = [[] for i in range(new_size)]
        for bucket in self.buckets:
            for i, (k, v) in enumerate(bucket):
                index = hash(k) % new_size
                new_buckets[index].append(bucket[i])
        self.buckets = new_buckets
        print("rehashing completed")

    def keys(self):
        all_keys = []
        for bucket in self.buckets:
            for k, v in bucket:
                all_keys.append(k)
        return all_keys

print("=== create hash_map")
hash_map = Hash_Map()
n = 12
value_range = n * 2

print("=== add key-value pairs to hash_map, rehash when full")
for i in range(n):
    k = random.randint(1, value_range)
    key, value = f"key_{k}", f"value_{k}"
    print(f"adding {key} -> {value}")
    hash_map[key] = value

print("=== search for random keys in hash_map")
for i in range(n):
    key = f"key_{random.randint(1, value_range)}"
    try:
        value = hash_map[key]
        print(f"Found: {key} -> {value}")
    except KeyError:
        print(f"{key} not found in hash map")

print("=== get each key from hash_map and delete it")
all_keys = hash_map.keys()
for key in all_keys:
    print(f"delete {key}")
    del hash_map[key]
