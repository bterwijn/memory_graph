import random

# show separate nodes for floats
mg.config.embedded_types -= {float} 
# show float as a table with Xs for size
mg.config.type_to_node[float] = lambda f : mg.Node_Table(f, 
                                [[str(f)]] + [['X']] * int(f) )
# show full table
mg.config.type_to_slicer[float] = (mg.Slicer(), mg.Slicer())

def cocktail_shaker_sort(data):
    start = 0
    end = len(data) - 1
    print('unsorted section:',start,'through',end)
    while True:
        swapped = False
        for i in range(start, end):
            a, b = data[i], data[i + 1]
            if a > b:
                data[i], data[i + 1] = b, a
                swapped = True
                new_end = i
        if not swapped:
            break
        end = new_end
        print('unsorted:', data)
        print('unsorted section:',start,'through',end)
        swapped = False
        for i in range(end, start, -1):
            a, b = data[i], data[i - 1]
            if a < b:
                data[i], data[i - 1] = b, a
                swapped = True
                new_start = i
        if not swapped:
            break
        start = new_start
        print('unsorted:', data)
        print('unsorted section:',start,'through',end)
  
n = 10
data = [float(i) for i in range(n)]
random.shuffle(data)
print('unsorted:', data)
cocktail_shaker_sort(data)
print('sorted:', data)
