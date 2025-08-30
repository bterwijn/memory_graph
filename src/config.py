# Some useful memory_graph configuration examples.
# Step through this file to see the effects.


# String Length

a = "hello world! " * 10
print(f'{mg.config.max_string_length=}') 
mg.config.max_string_length = 100  # set different max length 
mg.config_default.reset()


# Color (names: https://graphviz.org/doc/info/colors.html)

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]
print(f'{mg.config.type_to_color=}')
mg.config.type_to_color[list] = "red"       # set color for list type
mg.config.type_to_color[id(b)] = "green"    # set color for id
mg.config.type_to_color[id(c)] = "#1177FF"  # set RGB color for id
mg.config_default.reset()


# Orientation

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]
b.append([10, 11, 12])                     # vertical unless it has a reference
print(f'{mg.config.type_to_vertical=}')
mg.config.type_to_vertical[list] = False   # all lists horizontal
mg.config.type_to_vertical[list] = True    # all lists vertical
mg.config.type_to_vertical[list] = None    # back to vertical unless it has a reference
mg.config.type_to_vertical[id(c)] = False  # 'c' horizontal
mg.config_default.reset()


# Slicer

a = [1, 2, 3] * 10
b = [4, 5, 6] * 10
c = [7, 8, 9] * 10
print(f'{mg.config.type_to_slicer=}')
mg.config.type_to_slicer[list] = mg.Slicer(3)        # 3 element at start
mg.config.type_to_slicer[list] = mg.Slicer(3, 5)     # 5 at the end
mg.config.type_to_slicer[list] = mg.Slicer(3, 4, 5)  # 4 in the middle
mg.config.type_to_slicer[id(c)] = mg.Slicer()        # 'c' shows all
mg.config_default.reset()


# Embedded Types

a = [True, 42, 1.234, complex(3, 5), "hello world!", ]
print(f'{mg.config.embedded_types=}')
mg.config.embedded_types -= {bool, float, str}  # show separate nodes for types
mg.config_default.reset()
mg.config.embedded_types -= {int, complex}      # show separate nodes for types
mg.config_default.reset()


# Depth

c = []
b = [c]
a = [b]
del b, c
mg.config.type_to_depth[dict] = 2  # cut 2 levels below type 'dict'
c = a[0][0]                        # but now 'c' causes it to be a level 1
del a, c
mg.config_default.reset()


# Node Type

class MyClass:
    def __init__(self):
        self.x = 1
        self.y = 2
        self.z = 3
        
a = MyClass()

# show an object of type 'MyClass' as single value
mg.config.type_to_node[MyClass] = lambda data: mg.Node_Leaf(data,
                                         f'{data.x} {data.y} {data.z}')
# show an object of type  'MyClass' as a line of indexed values like a list
mg.config.type_to_node[MyClass] = lambda data: mg.Node_Linear(data,
                                         [data.x, data.y, data.z])
# show an object of type  'MyClass' as key-value pairs like a dict
mg.config.type_to_node[MyClass] = lambda data: mg.Node_Key_Value(data,
                                         {data.x:'x', data.y:'y', data.z:'z'}.items())
# show an object of type 'MyClass' as a table
mg.config.type_to_node[MyClass] = lambda data: mg.Node_Table(data,
                                         [[data.x, data.y],
                                          [data.z, 'X']])
mg.config_default.reset()
