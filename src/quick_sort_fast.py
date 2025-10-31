import memory_graph as mg
import random

class List_View:
    
    def __init__(self, values, begin, end):
        self.values, self.begin, self.end = values, begin, end

mg.config.type_to_node[List_View] = (lambda v: 
     mg.Node_Linear(v, [i if v.begin<= i<v.end else '' for i in v.values]
     if hasattr(v, 'end') else [])
)

mg.config.type_to_slicer[mg.Node_Linear] = mg.Slicer()

def cocktail_shaker_sort(values, begin, end):
    view = List_View(values, begin, end)
    end = end - 1
    while True:
        swapped = False
        for i in range(begin, end):
            a, b = values[i], values[i + 1]
            if a > b:
                values[i], values[i + 1] = b, a
                swapped = True
                new_end = i
        if not swapped:
            break
        end = new_end
        swapped = False
        for i in range(end, begin, -1):
            a, b = values[i], values[i - 1]
            if a < b:
                values[i], values[i - 1] = b, a
                swapped = True
                new_start = i
        if not swapped:
            break
        begin = new_start

def quick_sort(values, begin, end):
    view = List_View(values, begin, end)
    if begin >= end - 1:
        return
    if begin == end - 2:
        if values[end-1] < values[begin]:
            values[begin], values[end-1] = values[end-1], values[begin]
        return
    if begin >= end - 4:
        cocktail_shaker_sort(values, begin, end)
        return
    pivot_i = random.randrange(begin, end)
    pivot   = values[pivot_i]
    smaller = sum(1 * (values[i]<pivot) for i in range(begin, end))
    new_pivot_i = begin+smaller
    values[new_pivot_i], values[pivot_i] = values[pivot_i], values[new_pivot_i]
    if new_pivot_i - begin < end - new_pivot_i - 1:
        j = new_pivot_i + 1
        for i in range(begin, new_pivot_i):
            if not values[i] < pivot:
                while True:
                    if values[j] < pivot:
                        break
                    j += 1
                values[i], values[j] = values[j], values[i]
    else:
        for i in range(new_pivot_i+1, end):
            j = begin
            if values[i] < pivot:
                while True:
                    if not values[j] < pivot:
                        break
                    j += 1
                values[i], values[j] = values[j], values[i]         
    quick_sort(values, begin, new_pivot_i)
    quick_sort(values, new_pivot_i+1, end)

n = 12
values = list(range(n))
random.shuffle(values)
print('unsorted values:',values)
quick_sort(values, 0, len(values))
print('  sorted values:',values)
