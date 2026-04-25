import random
NR_BITS = 3
NR_VALUES = 1 << NR_BITS 
BIT_MASK = NR_VALUES - 1

def counting_sort(data, data_new, bit_block):
    """ Sorts `data` to the digit at position `digit` using stable
    Counting Sort. The sorted data is writen to `data_new`. """
    counts = [0] * NR_VALUES
    for d in data:
        counts[(d >> (bit_block * NR_BITS)) & BIT_MASK] += 1
    for i in range(1, len(counts)):
        counts[i] += counts[i - 1]
    for i in range(len(data) - 1, -1, -1):
        d = (data[i] >> (bit_block * NR_BITS)) & BIT_MASK
        counts[d] -= 1
        data_new[counts[d]] = data[i]

def radix_sort(data, bit_blocks):
    """ Sorts `data` using radix sort. The number of digits in the largest 
    number is `nr_digits`. """
    data_new = [0] * len(data)
    for bit_block in range(bit_blocks):
        counting_sort(data, data_new, bit_block)
        data, data_new = data_new, data
    return data

def get_random_data(n, bit_blocks):
    """ Generates a list of `n` random integers with 
    `bit_blocks` x `NR_BITS` bits. """
    range_end = 1 << (bit_blocks * NR_BITS)
    return [random.randrange(range_end) for _ in range(n)]

n = 15
bit_blocks = 3
data = get_random_data(n, bit_blocks)
print('data:', data)
data_sorted = radix_sort(data, bit_blocks)  # corrupts 'data' 
print('data_sorted:', data_sorted)
