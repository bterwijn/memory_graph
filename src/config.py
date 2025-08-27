# Some useful memory_graph configurations.
# Step through this file to see the effects.


# Setting string length

a = "hello world! " * 10
print(f'{mg.config.max_string_length=}') 
mg.config.max_string_length = 100  # set different max length 
mg.config_default.reset()


# Showing nodes for embedded types

a = [True, 42, 1.234, complex(3, 5), "hello world!", ]
print(f'{mg.config.embedded_types=}')
mg.config.embedded_types -= {bool, float, str}  # show separate nodes
mg.config_default.reset()


# Changing color

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]
print(f'{mg.config.type_to_color=}')
mg.config.type_to_color[list] = "red"     # set list color for type
mg.config.type_to_color[id(c)] = "green"  # set list color for id
mg.config_default.reset()


# Orientation

b.append([10, 11, 12])                  # vertical unless it has a reference
print(f'{mg.config.type_to_vertical=}')
mg.config.type_to_color[list] = False   # all lists horizontal
mg.config.type_to_color[list] = True    # all lists vertical
mg.config.type_to_color[id(c)] = False  # 'c' horizontal
mg.config_default.reset()


