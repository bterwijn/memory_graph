# Graph your Memory #

Want to draw a graph of your data in Python to better understand its
structure or the Python memory model in general?

Just call `memory_graph.show(your_data)`, an example:

```
import memory_graph

data = [ (1, 2), [3, 4], {5:'five', 6:'six'} ]
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

## Graph all Local Variables ##

Often it is useful to graph all the local variables using:

```
memory_graph.show( locals(), block=True )
```

Also useful to set as 'watch' in a debugger tool:

```
memory_graph.render( locals(), "my_debug_graph.pdf" )
```

## Larger Example ##

This larger example shows objects that share a class (static) variable and
also shows we can handle recursive references just fine.

```
import memory_graph

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

memory_graph.show( locals() )
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example2.png)


## Install ##

Install using pip:

```
pip install memory-graph
```

## Config ##

Different aspects of memory_graph can be configured.

### Config Visualization, graphviz_nodes ###

Configure how the nodes of the graph are visualized with:

- ***memory_graph.graphviz_nodes.layout_vertical*** : bool
  - determines if list/tuple/... are drawn vertically
- ***memory_graph.graphviz_nodes.type_category_to_color_map*** : dict
  - a mapping from type to color
- ***memory_graph.graphviz_nodes.uncategorized_color*** : string
  - color used for uncategorized types
- ***memory_graph.graphviz_nodes.padding*** : int
  - amount of padding for node cells
- ***memory_graph.graphviz_nodes.spacing*** : int
  - amount of spacing for node cells
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

- ***memory_graph.rewrite_to_node.reduce_reference_types*** : set
  - the types we add to a node instead of drawing a reference to it
- ***memory_graph.rewrite_to_node.reduce_references_for_classes*** : bool
  - determines if we reduce the reference (to dictionary) for classes

### Config Node Creation, rewrite ###

Configure what nodes are created based on reading the given data structure:

- ***memory_graph.rewrite.ignore_types*** : set
  - all types that we ignore, these will not be in the graph
- ***memory_graph.rewrite.singular_types*** : set
  - all types rewritten to node as singular values (bool, int, float, ...)
- ***memory_graph.rewrite.linear_types*** : set
  - all types rewritten to node as linear values (tuple, list, set, ...)
- ***memory_graph.rewrite.dict_types*** : set
  - all types rewritten to node as dictionary values (dict, mappingproxy)
- ***memory_graph.rewrite.dict_ignore_dunder_keys*** : bool
  - determines if we ignore dunder keys ('`__example`') in dict_types
- ***memory_graph.rewrite.rewrite_generators*** : bool
  - determines if we read and rewrite a generator to node
- ***memory_graph.rewrite.rewrite_any_iterable*** : bool
  - determines if we rewrite any iterable to node

### Config example ###

With configuration:
```
memory_graph.graphviz_nodes.layout_vertical = False                       # draw lists,tuples,sets,... horizontally
memory_graph.graphviz_nodes.type_category_to_color_map['list'] = 'yellow' # change color of 'list' type
memory_graph.graphviz_nodes.spacing=15                                    # more spacing in each node
memory_graph.graphviz_nodes.graph_attr['ranksep']='1.2'                   # more vertical separation
memory_graph.graphviz_nodes.graph_attr['nodesep']='1.2'                   # more horizontal separation
memory_graph.rewrite_to_node.reduce_reference_types.remove(int)           # draw references to 'int' type
```

the last example looks like:

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example3.png)


## Troubleshooting ##

When edges overlap it can be hard to distinguish them. Using an
interactive graphviz viewer, such as
[xdot](https://github.com/jrfonseca/xdot.py), on a '*.gv' output file
will help.


## Author ##
Bas Terwijn


## Inspiration ##
Inspired by [PythonTutor](https://pythontutor.com/visualize.html).
