import random

def get_digit(i, d):
    """ Get digit number 'd' from 'i' where 'd=0' is the right most digit. """
    return (i // 10**d) % 10

def counting_sort(new_data, data, digit):
    counts = [0] * 10
    data_digits = [get_digit(i, digit) for i in data]
    for d in data_digits:
        counts[d] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    for i in range(len(data) - 1, -1, -1):
        d = data_digits[i]
        counts[d] -= 1
        new_data[counts[d]] = data[i]

def radix_sort(data, nr_digits):
    new_data = data.copy()
    for d in range(nr_digits):
        counting_sort(new_data, data, d)
        data, new_data = new_data, data
    return data

def get_random_data(n, nr_digits):
    range_end = 10**nr_digits
    return  [random.randrange(range_end) for _ in range(n)]

n = 25
nr_digits = 3
data = get_random_data(n, nr_digits)
print('data:', data)
data_sorted = radix_sort(data, nr_digits)
print('data_sorted:', data_sorted)
