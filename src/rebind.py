def add_one(a, b):
    a += 1     # change remains confined to 'a' in the add_one function
    b[0] += 1  # change also affects 'b' outside of the add_one function

a = 10
b = [10]  # wrap in a value of mutable type list
add_one(a, b)

print(f"a:{a} b:{b[0]}")
