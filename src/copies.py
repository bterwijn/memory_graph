import copy

a = [ [1, 2], ['x', 'y'] ]  # a nested list (a list containing lists)

# three different ways to make a "copy" of 'a':
c1 = a
c2 = copy.copy(a)  # equivalent to:  a.copy() a[:] list(a)
c3 = copy.deepcopy(a)
