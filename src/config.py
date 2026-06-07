# Some useful memory_graph configuration examples.
# Step through this file to see the effects.

import memory_graph as mg
print('memory_graph version:', mg.__version__)


# String Length

a = "hello world! " * 10
print(f'{mg.config.max_string_length=}') 
mg.config.max_string_length = 100  # set different max length 
mg.config_default.reset()
del a


# Type Labels

a = [1, 2]
b = (3, 4)
c = {5, 6}
print(f'{mg.config.type_labels=}')
mg.config.type_labels = False  # no type labels
mg.config_default.reset()
del a, b, c


# Color (names: https://graphviz.org/doc/info/colors.html)

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]
print(f'{mg.config.type_to_color=}')
mg.config.type_to_color[list] = "red"       # set color for list type
mg.config.type_to_color[id(b)] = "green"    # set color for id
mg.config.type_to_color[id(c)] = "#1177FF"  # set RGB color for id
mg.config_default.reset()
del a, b, c


# Orientation

a = [1, 2, 3]
b = [4, 5, 6]
c = [7, 8, 9]
b.append([10, 11, 12])                      # vertical unless it has a reference
print(f'{mg.config.type_to_horizontal=}')
mg.config.type_to_horizontal[list] = True   # all lists horizontal
mg.config.type_to_horizontal[list] = False  # all lists vertical
mg.config.type_to_horizontal[list] = None   # back to vertical unless it has a reference
mg.config.type_to_horizontal[id(c)] = True  # 'c' horizontal
mg.config_default.reset()
del a, b, c


# Slicer

a = [1, 2, 3] * 10
b = [4, 5, 6] * 10
c = [7, 8, 9] * 10
print(f'{mg.config.type_to_slicer=}')
mg.config.type_to_slicer[list]  = mg.Slicer(3)        # 3 elements at start
mg.config.type_to_slicer[list]  = mg.Slicer(3, 5)     # 5 at the end
mg.config.type_to_slicer[list]  = mg.Slicer(3, 4, 5)  # 4 in the middle
mg.config.type_to_slicer[id(c)] = mg.Slicer()         # 'c' shows all
mg.config_default.reset()
del a, b, c


# Embedded Types

a = [True, 42, 1.234, complex(3, 5), "hello world!", ]
print(f'{mg.config.embedded_types=}')
mg.config.embedded_types -= {bool, float, str}  # show separate nodes for types
mg.config_default.reset()
mg.config.embedded_types -= {int, complex}      # show separate nodes for types
mg.config_default.reset()
del a


# Depth

c = []
b = [c]
a = [b]
del b, c
mg.config.type_to_depth[dict] = 2  # cut 2 levels below type 'dict'
c = a[0][0]                        # but now 'c' is at level 1
mg.config_default.reset()
del a, c


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

mg.collapse_type(MyClass) # collapse type for graph readability and performance
mg.reset_type(MyClass)    # reset to default introspection

mg.config_default.reset()
del MyClass, a


# Exceptions

mylist = [0, 1]
try:
    mylist[2]
except Exception as e:
    print(e)
    # choose shorter string representation for BaseException
    mg.config.type_to_string[BaseException] = lambda e: mg.utils.exception_to_string_short(e)
    print(mg.utils.exception_to_string_short(e))

mg.config_default.reset()
del mylist


# Strings

import string
normal_str   = '\n'.join([string.ascii_lowercase] * 3)
full_str     = mg.full_str(normal_str)      # no size limit
unquoted_str = mg.unquoted_str(normal_str)  # no quotes
html_str     = mg.html_str("""
<TABLE BORDER="1">
  <TR><TD>  <B>c1</B>                    </TD><TD>  <I>c2</I>                       </TD></TR>
  <TR><TD>  <S>c3</S>                    </TD><TD>  <FONT FACE="Courier">c4</FONT>  </TD></TR>
  <TR><TD>  <U>c5</U>                    </TD><TD>  <O>c6</O>                       </TD></TR>
  <TR><TD>  <FONT COLOR="red">c7</FONT>  </TD><TD>  <FONT COLOR="green">c8</FONT>   </TD></TR>
</TABLE>
""")  # Grahviz html-like: https://graphviz.org/doc/info/shapes.html#html

del normal_str, full_str, unquoted_str, html_str


# Font

import string
lower = string.ascii_lowercase
upper = string.ascii_uppercase
punctuation = string.punctuation

print(f'{mg.config.fontname=}')
print(f'{mg.config.fontsize=}')

# These might do well in SVG on the web, it varies per system:
webfonts = ['Courier', 'Monaco', 'Arial', 'Helvetica', 'Verdana', 'Tahoma', 'Geneva', 'Times', 'Times-Roman', 'Georgia', 'Palatino']
for font in webfonts:
    print('Trying font:', font)
    mg.config.fontname = font      # change font name
# If not, right-click the graph to save and view it locally.

mg.config.fontsize = '32'          # change font size

mg.config_default.reset()
del lower, upper, punctuation, webfonts, font
