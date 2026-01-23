import memory_graph as mg

a = [100, 200]
b = a
mg.render(locals(), 'rebinding1.png')

b += [300]      # changes value of 'b' and 'a'
b = [400, 500]  # rebinds 'b' to a new value, 'a' is uneffected
c = b
mg.render(locals(), 'rebinding2.png')

c = b + [600]   # rebinds 'c' to new value 'b + [600]', `b` is unaffected
mg.render(locals(), 'rebinding3.png')
