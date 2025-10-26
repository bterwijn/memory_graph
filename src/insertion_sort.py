import random

mg.config.embedded_types -= {float}  # show separate nodes for floats

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i
        while j > 0:
            smaller = data[j-1]
            if smaller < key:
                break
            j -= 1
        if j < i:
            print('swapping', data[j:i], 'with', key)
            data[j+1:i+1] = data[j:i]; data[j] = key
            print('unsorted:', data)

n = 10
data = [float(i) for i in range(n)]
random.shuffle(data)
print('unsorted:', data)
insertion_sort(data)
print('sorted:', data)
