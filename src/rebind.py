a = [4, 3, 2]
b = a

b += [1]        # changes the value of 'b' and 'a'
b = [100, 200]  # rebinds 'b' to another value, 'a' is unaffected
c = b

c = b + [300]   # rebinds 'c' to new value 'b + [300]', `b` is unaffected

print(f'{a=}\n{b=}\n{c=}')
