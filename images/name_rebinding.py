import memory_graph as mg

a = [4, 3, 2]
b = a
mg.render(locals(), 'rebinding1.png')

a += [1]        # changes value of 'a' and 'b'
a = [100, 200]  # rebinds 'a' to a new value, 'b' is uneffected
mg.render(locals(), 'rebinding2.png')
