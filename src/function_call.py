def add_one(a, b, c):
    a += [1]
    b += (1,)
    c += [1]

a = [4, 3, 2]
b = (4, 3, 2)
c = [4, 3, 2]
add_one(a, b, c.copy())

print(f"a:{a} b:{b} c:{c}")
