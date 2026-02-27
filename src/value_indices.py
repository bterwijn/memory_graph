import random

n = 20
values = [random.randrange(n) for i in range(n)]
print(f'{values=}')

value_to_indices = {}
for index, value in enumerate(values):
    if not value in value_to_indices:
        value_to_indices[value] = []
    value_to_indices[value].append(index)
print(f'{value_to_indices=}')

print(f'value indices')
for value, indices in value_to_indices.items():
    print(f'{value:5} {indices}')

