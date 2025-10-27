import random

# show separate nodes for floats
mg.config.embedded_types -= {float} 
# show float as a table with Xs for size
mg.config.type_to_node[float] = lambda f : mg.Node_Table(f, 
                                [[str(f)]] + [['X']] * int(f) )
# show full table
mg.config.type_to_slicer[float] = (mg.Slicer(), mg.Slicer())

def selection_sort(data):
    for i in range(len(data)):
        replace = data[i]
        min_index = i
        min_value = replace
        for j in range(i + 1, len(data)):
            value = data[j]
            if value < min_value:
                min_index = j
                min_value = value
        data[i], data[min_index] = min_value, replace

n = 10
data = [float(i) for i in range(n)]
random.shuffle(data)
print('unsorted:', data)
selection_sort(data)
print('sorted:', data)
