# Graph your Memory #

Want to draw a graph of your data in Python to better understand its
structure or the Python memory model in general?

Just call `memory_graph.show( your_data )`, an example:
```
data = [ (1, 2), [3, 4], {5:'five', 6:'six'} ]

import memory_graph
memory_graph.show( data, block=True )
```
This shows the graph with the starting point of your 'data' drawn
using thick lines, the program blocks until the ENTER key is pressed.

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example1.png)

If `show()` doesn't work well on your system (the PDF viewer
integration is platform specific) use `render()` to output the graph
in the format of your choosing and open it yourself.

```
memory_graph.render( data, "my_graph.png", block=True )
```

## Install ##

Install using pip:
```
pip install memory-graph
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.


## Graph all Local Variables ##

Often it is useful to graph all the local variables using:
```
memory_graph.show( locals(), block=True )
```

So much so that function `d()` is available as alias for easier
debugging. Additionally it logs all locals by printing them which
allows for comparing them over time. For example:
```
from memory_graph import d

my_squares = []
my_squares_ref = my_squares
for i in range(5):
    my_squares.append(i**2)
    d()                                    # 'd' for debug, logs and graphs all local variables and blocks
my_squares_copy = my_squares.copy()
d(block=False)                             # debug without blocking
d(log=False,block=False)                   # debug without logging and blocking

import memory_graph
memory_graph.log_file=open("log.txt","w")  # now log to file instead of screen (sys.stdout)
d(graph=False)                             # debug without showing the graph
```

Which in the end results in:

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example2.png)
```
my_squares: [0, 1, 4, 9, 16]
my_squares_ref: [0, 1, 4, 9, 16]
i: 4
my_squares_copy: [0, 1, 4, 9, 16]
```

Notice that in the graph it is clear that 'my_squares' and
'my_squares_ref' share their data while 'my_squares_copy' has its own
copy. This can not be observed in the log and shows the benefit
of the graph.

Alternatively debug by setting this expression as 'watch' in a
debugger tool and open the output file:
```
memory_graph.render( locals(), "my_debug_graph.pdf" )
```


## Larger Example ##

This larger example shows objects that share a class (static) variable
and also shows we can handle recursive references although the graph
layout might suffer a bit.
```
my_list = [10, 20, 10]

class My_Class:
    my_class_var = 20 # class variable: shared by different objects
    
    def __init__(self):
        self.var1 = "foo"
        self.var2 = "bar"
        self.var3 = 20

obj1 = My_Class()
obj2 = My_Class()

data=[my_list, my_list, obj1, obj2]

my_list.append(data) # recursive reference

import memory_graph
memory_graph.show( locals() )
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example3.png)


## Config ##

Different aspects of memory_graph can be configured.

### Config Visualization, graphviz_nodes ###

Configure how the nodes of the graph are visualized with:

- ***memory_graph.graphviz_nodes.linear_layout_vertical*** : bool
  - if False, linear node layout is horizontal
- ***memory_graph.graphviz_nodes.linear_any_ref_layout_vertical*** : bool
  - if False, linear node layout is horizontal if any of its elements is a refence
- ***memory_graph.graphviz_nodes.linear_all_ref_layout_vertical*** : bool
  - if False, linear node layout is horizontal if all elements are reference
- ***memory_graph.graphviz_nodes.key_value_layout_vertical*** : bool
  - if False, key_value node layout is horizontal
- ***memory_graph.graphviz_nodes.key_value_any_ref_layout_vertical*** : bool
  - if False, key_value node layout is horizontal if any of its elements is a refence
- ***memory_graph.graphviz_nodes.key_value_all_ref_layout_vertical*** : bool
  - if False, key_value node layout is horizontal if all elements are reference
- ***memory_graph.graphviz_nodes.padding*** : int
  - the padding in nodes
- ***memory_graph.graphviz_nodes.padding*** : int
  - the spacing in nodes
- ***memory_graph.graphviz_nodes.join_references_count*** : int
  - minimum number of reference we join together
- ***memory_graph.graphviz_nodes.join_circle_size*** : string
  - size of the join circle
- ***memory_graph.graphviz_nodes.join_circle_minlen*** : string
  - extra space for references above a join circle
- ***memory_graph.graphviz_nodes.max_string_length*** : int
  - maximum string length where the string is cut off
- ***memory_graph.graphviz_nodes.category_to_color_map*** : dict
  - mapping van type/caterogries to node colors
- ***memory_graph.graphviz_nodes.uncategorized_color*** : dict
  - color for unkown types/categories
- ***memory_graph.graphviz_nodes.graph_attr*** : dict
  - allows to set various [graphviz graph attributes](https://graphviz.org/docs/graph/)
- ***memory_graph.graphviz_nodes.node_attr*** : dict
  - allows to set various [graphviz node attributes](https://graphviz.org/docs/nodes/)
- ***memory_graph.graphviz_nodes.edge_attr*** : dict
  - allows to set various [graphviz edges attributes](https://graphviz.org/docs/edges/)

See for color names: [graphviz colors](https://graphviz.org/doc/info/colors.html)

To configure more about the visualization use:
```
digraph = memory_graph.create_graph( locals() )
```
and see the [graphviz api](https://graphviz.readthedocs.io/en/stable/api.html) to render it in many different ways.

### Config Graph Structure, rewrite_to_node ###

Configure the structure of the nodes in the graph with:

- ***memory_graph.rewrite_to_node.reduce_reference_parents*** : set
  - the node types/categories for which we remove the reference to children
- ***memory_graph.rewrite_to_node.reduce_reference_children*** : bool
  - the node types/categories for which we remove the reference from parents
  
### Config Node Creation, rewrite ###

Configure what nodes are created based on reading the given data structure:

- ***memory_graph.rewrite.ignore_types*** : dict
  - all types that we ignore, these will not be in the graph
- ***memory_graph.rewrite.singular_types*** : set
  - all types rewritten to node as singular values (bool, int, float, ...)
- ***memory_graph.rewrite.linear_types*** : set
  - all types rewritten to node as linear values (tuple, list, set, ...)
- ***memory_graph.rewrite.dict_types*** : set
  - all types rewritten to node as dictionary values (dict, mappingproxy)
- ***memory_graph.rewrite.dict_ignore_dunder_keys*** : bool
  - determines if we ignore dunder keys ('`__example`') in dict_types
- ***memory_graph.rewrite.custom_accessor_functions*** : dict
  - custom accessor functions to defined how to read various types


### Config Examples ###

With configuration:
```
memory_graph.graphviz_nodes.linear_layout_vertical = False           # draw lists,tuples,sets,... horizontally
memory_graph.graphviz_nodes.category_to_color_map['list'] = 'yellow' # change color of 'list' type
memory_graph.graphviz_nodes.spacing=15                               # more spacing in each node
memory_graph.graphviz_nodes.graph_attr['ranksep']='1.2'              # more vertical separation
memory_graph.graphviz_nodes.graph_attr['nodesep']='1.2'              # more horizontal separation
memory_graph.rewrite_to_node.reduce_reference_children.remove("int") # draw references to 'int' type
```

the last example looks like:

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example4.png)


### Custom Accessor Functions ###

For any type a custom accessor function can be introduced. For example
Panda DataFrames and Series are not visualized correctly by
default. This can be fixed by adding custom accessor functions:

```
import pandas as pd

data = {'Name':['Tom', 'Anna', 'Steve', 'Lisa'],
        'Age':[28,34,29,42],
        'Length':[1.70,1.66,1.82,1.73] }
df = pd.DataFrame(data)

import memory_graph
memory_graph.rewrite.custom_accessor_functions[pd.DataFrame] = lambda d: list(d.items())
memory_graph.rewrite.custom_accessor_functions[pd.Series] = lambda d: list(d.items())
memory_graph.rewrite_to_node.reduce_reference_parents.add("DataFrame")
memory_graph.rewrite_to_node.reduce_reference_parents.add("Series")
memory_graph.graphviz_nodes.category_to_color_map['Series'] = 'lightskyblue'
memory_graph.show( locals() )
```

which results in:

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example5.png)

## Troubleshooting ##

When edges overlap it can be hard to distinguish them. Using an
interactive graphviz viewer, such as
[xdot](https://github.com/jrfonseca/xdot.py), on a '*.gv' output file
will help.


## Author ##
Bas Terwijn


## Inspiration ##
Inspired by [PythonTutor](https://pythontutor.com/).
