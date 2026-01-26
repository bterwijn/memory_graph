a = [100, 200]
b = a

b += [300]      # changes the value of 'b' and 'a'
b = [400, 500]  # rebinds 'b' to a new value, 'a' is unaffected
c = b

c = c + [300]   # rebinds 'c' to new value 'c + [300]', `b` is unaffected
print(f'{a=}\n{b=}\n{c=}')
