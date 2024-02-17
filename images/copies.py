import memory_graph
import copy

a = [ [1, 2], ['a', 'b'] ]

# three different ways to make a "copy" of a:
c1 = a
c2 = copy.copy(a) # equivalent:  a.copy() a[:]
c3 = copy.deepcopy(a)

memory_graph.render(locals(), 'copies.png')
