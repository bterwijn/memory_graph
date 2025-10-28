import random

# show separate nodes for floats
mg.config.embedded_types -= {float} 
# show float as a table with Xs for size
mg.config.type_to_node[float] = lambda f : mg.Node_Table(f, 
                                [[str(f)]] + [['X']] * int(f) )
# show full table
mg.config.type_to_slicer[float] = (mg.Slicer(), mg.Slicer())

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
