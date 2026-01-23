a = [100, 200]
b = a

b += [300]      # changes the value of 'b' and 'a'
b = [400, 500]  # rebinds 'b' to a new value, 'a' is unaffected
c = b

c = b + [600]   # rebinds 'c' to new value 'b + [600]', `b` is unaffected

print(f'{a=}\n{b=}\n{c=}')
