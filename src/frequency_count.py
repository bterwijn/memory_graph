import random

def get_frequency_counts(values):
    """ Returns a dict value->counts of 'values'. """
    counts = {}
    for v in values:
        counts[v] = counts.get(v, 0) + 1
    return counts

def show_counts(value_range, counts):
    """ Show 'counts' for int values from 0 to 'value_range'. """
    for i in range(value_range):
        print(f'{i:3}', '#' * counts.get(i, 0))

value_range = 5
nr_values = value_range * 2
values = [random.randrange(value_range) for _ in range(nr_values)]
print('values:', values)

counts = get_frequency_counts(values)
print('counts:', counts)
show_counts(value_range, counts)
