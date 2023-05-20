# Graph your Memory #

Want to draw a graph of your data in Python to better understand its
structure or the Python memory model in general?

Just call `memory_graph.show(your_data)`, an example:

```
import memory_graph

data = [ (1, 2), [3, 4], {5:'five', 6:'six'} ]
memory_graph.show( data )
```

This shows the graph with the starting point of your 'data' drawn
using thick lines, the program blocks until the ENTER key is pressed.

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example1.png)

If `show()` doesn't work well on your system (the PDF viewer
integration is platform specific) use `render()` to output the graph
in the format of your choosing. Use `block=False` to turn off
blocking.

```
memory_graph.render( data, "my_graph.png", block=False )
```

## Larger Example ##

This larger example shows objects that share a class (static) variable and
also shows we can handle recursive references just fine.

```
import memory_graph

my_list = [10, 20, 30]

class My_Class:
    my_class_var = 1000 # class variable: shared by different objects
    
    def __init__(self):
        self.var1 = "foo"
        self.var2 = "bar"

obj1 = My_Class()
obj2 = My_Class()

data=[my_list, my_list, obj1, obj2]

my_list.append(data) # recursive reference

memory_graph.show( data )
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example2.png)

Often it is useful to show all local variables using:

```
memory_graph.show( memory_graph.filter(locals()) )
```

## Install ##

Install using pip:

```
pip install memory-graph
```

## Config ##

Different aspects of memory_graph can be configured.

### Config visualization, graphviz_nodes ###

Configure how the nodes of the graph are visualized with:

- ***memory_graph.graphviz_nodes.layout_vertical*** : bool
  - determines if list/tuple/... are drawn vertically
- ***memory_graph.graphviz_nodes.type_category_to_color_map*** : dict
  - a mapping from type to color
- ***memory_graph.graphviz_nodes.uncategorized_color*** : string
  - color used for uncategorized types

See for color names: [graphviz colors](https://graphviz.org/doc/info/colors.html)

To configure more about the visualization use:
```
digraph = memory_graph.create_graph( memory_graph.filter(locals()) )
```
and see the [graphviz api](https://graphviz.readthedocs.io/en/stable/api.html) to render it in many different ways.

### Config node structure, rewrite_to_node ###

Configure the structure of the nodes in the graph with:

- ***memory_graph.rewrite_to_node.reduce_reference_types*** : set
  - the types we copy to a node instead of drawing a reference to it
- ***memory_graph.rewrite_to_node.reduce_references_for_classes*** : bool
  - determines if we reduce the references (to dict) in objects of classes
- ***memory_graph.rewrite_to_node.class_variables_label*** : str
  - the label used to reference the class varibles (mappingproxy)

### Config node creation, rewrite ###

Configure what nodes are created based on reading the given data structure:

- ***memory_graph.rewrite.singular_types*** : set
  - all types rewritten to node as singular values (bool, int, float, ...)
- ***memory_graph.rewrite.linear_types*** : set
  - all types rewritten to node as linear values (tuple, list, set, ...)
- ***memory_graph.rewrite.dict_types*** : set
  - all types rewritten to node as dictionary values (dict, mappingproxy)

### Config example ###

With configuration:
```
memory_graph.graphviz_nodes.layout_vertical = True                        # draw list/tuple/set/... vertically
memory_graph.graphviz_nodes.type_category_to_color_map['list'] = 'yellow' # change color of 'list' types
memory_graph.rewrite_to_node.reduce_reference_types.remove(int)           # draw references to 'int' types
```
the last example looks like:
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example3.png)


## Author ##
Bas Terwijn


## Inspiration ##
Inspired by [PythonTutor](https://pythontutor.com/visualize.html).
