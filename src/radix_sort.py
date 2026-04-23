import random
BASE = 10

def counting_sort(data, data_new, digit):
    """ Sorts `data` to the digit at position `digit` using stable
    Counting Sort. The sorted data is writen to `data_new`. """
    counts = [0] * BASE
    exp = BASE ** digit
    for d in data:
        counts[(d // exp) % BASE] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    for i in range(len(data) - 1, -1, -1):
        d = (data[i] // exp) % BASE
        counts[d] -= 1
        data_new[counts[d]] = data[i]

def radix_sort(data, nr_digits):
    """ Sorts `data` using radix sort. The number of digits in the largest 
    number is `nr_digits`. """
    data_new = [0] * len(data)
    for d in range(nr_digits):
        counting_sort(data, data_new, d)
        data, data_new = data_new, data
    return data

def get_random_data(n, nr_digits):
    """ Generates a list of `n` random integers with `nr_digits` digits. """
    range_end = BASE ** nr_digits
    return  [random.randrange(range_end) for _ in range(n)]

n = 15
nr_digits = 3
data = get_random_data(n, nr_digits)
print('data:', data)
data_sorted = radix_sort(data, nr_digits)  # corrupts 'data' 
print('data_sorted:', data_sorted)
