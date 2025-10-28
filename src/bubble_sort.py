import random

# show separate nodes for floats
mg.config.embedded_types -= {float} 
# show float as a table with Xs for size
mg.config.type_to_node[float] = lambda f : mg.Node_Table(f, 
                                [[str(f)]] + [['X']] * int(f) )
# show full table
mg.config.type_to_slicer[float] = (mg.Slicer(), mg.Slicer())

def bubble_sort_section(data, begini, endi):
    swapped = False
    last_swapi = 0
    for i in range(begini, endi):
        a = data[i]
        b = data[i+1]
        if a > b:
            data[i], data[i+1] = b, a
            if not swapped:
                swapped = True
                begini = max(i-1, 0)
            last_swapi = i
    return begini, last_swapi

def bubble_sort(data):
    begini, endi = 0, len(data)-1
    while True:
        print('sorting section', begini, 'through', endi)
        begini, endi = bubble_sort_section(data, begini, endi)
        if begini >= endi:
            break
        print('unsorted:', data)

n = 10
data = [float(i) for i in range(n)]
random.shuffle(data)
print('unsorted:', data)
bubble_sort(data)
print('sorted:', data)
