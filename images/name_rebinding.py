import memory_graph as mg

a = [4, 3, 2]
b = a
mg.render(locals(), 'rebinding1.png')

b += [1]        # changes value of 'b' and 'a'
b = [100, 200]  # rebinds 'b' to a new value, 'a' is uneffected
mg.render(locals(), 'rebinding2.png')
