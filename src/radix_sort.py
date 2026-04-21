import random

def counting_sort(new_data, data, digit):
    """ Sorts `data` to the digit at position `digit` using 
    Counting Sort. The sorted data is writen to `new_data`. """
    counts = [0] * 10
    exp = 10 ** digit
    data_digits = [(value // exp) % 10 for value in data]
    for d in data_digits:
        counts[d] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    for i in range(len(data) - 1, -1, -1):
        d = data_digits[i]
        counts[d] -= 1
        new_data[counts[d]] = data[i]

def radix_sort(data, nr_digits):
    """ Sorts `data` using radix sort. The number of digits in the largest 
    number is `nr_digits`. """
    new_data = data.copy()
    for d in range(nr_digits):
        counting_sort(new_data, data, d)
        data, new_data = new_data, data
    return data

def get_random_data(n, nr_digits):
    """ Generates a list of `n` random integers with `nr_digits` digits. """
    range_end = 10**nr_digits
    return  [random.randrange(range_end) for _ in range(n)]

n = 15
nr_digits = 3
data = get_random_data(n, nr_digits)
print('data:', data)
data = radix_sort(data, nr_digits)
print('data_sorted:', data)
