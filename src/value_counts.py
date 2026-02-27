import random

n = 20
values = [random.randrange(n) for i in range(n)]
print(f'{values=}')

counts = {}
for v in values:
    if not v in counts:
        counts[v] = 0
    counts[v] += 1
print(f'{counts=}')

print(f'value count')
for value, count in counts.items():
    print(f'{value:5} {count:5}')

