a = [4, 3, 2]
b = a

b += [1]        # changes the value of 'b' and 'a'
b = [100, 200]  # rebinds 'b' to a new value, 'a' is unaffected
c = b

c = c + [300]   # rebinds 'c' to new value 'c + [300]', `b` is unaffected

print(f'{a=}\n{b=}\n{c=}')
