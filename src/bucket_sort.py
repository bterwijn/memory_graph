import random

class Bucket_Sort:
    
    def __init__(self, data, nr_buckets):
        min_val, max_val = min(data), max(data)
        if min_val == max_val:
            self.buckets = [ data ]
        else:
            self.buckets = [ [] for _ in range(nr_buckets)]
            bucket_size = (max_val - min_val) / nr_buckets
            for i in data:
                b = int((i - min_val) // bucket_size)
                b = min(b, nr_buckets-1)
                self.buckets[b].append(i)
            for bi in range(len(self.buckets)):
                if len(self.buckets[bi]) > 1:
                    self.buckets[bi] = Bucket_Sort(self.buckets[bi], nr_buckets)

    def get_sorted_data(self):
        
        def get_sorted_data_recursive(self, data):
            for b in self.buckets:
                if isinstance(b, Bucket_Sort):
                    get_sorted_data_recursive(b, data)
                else:
                    data.extend(b)
            
        data = []
        get_sorted_data_recursive(self, data)
        return data
        
def get_random_data(n, rand_range):
    """ Generates a list of `n` random integers in range [rand_min,rand_max). """
    return [random.randrange(rand_range) for _ in range(n)]

n = 15
rand_range = 1000
nr_buckets = 5
data = get_random_data(n, rand_range)
print('data:', data)
bucket_sort = Bucket_Sort(data, nr_buckets)
data = bucket_sort.get_sorted_data()
print('data_sorted:', data)
