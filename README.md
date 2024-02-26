## Installation ##
Install `memory_graph` using pip:
```
pip install memory-graph
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.


# Graph your Memory #
Does your Python code have a bug, is it behaving differently from what you expect? The problem could be a misunderstanding of the Python Data Model, and the first step to the solution could be drawing your data as a graph using `memory_graph.show( your_data )`, an example:
```python
import memory_graph

data = [ (1, 2), [3, 4], {5, 6}, {7:'seven', 8:'eight'} ]
memory_graph.show(data, block=True)
```
This shows a graph with the starting point of our 'data' drawn with thick lines, the program blocks until the ENTER key is pressed.

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example1.png)


Alternatively render the graph to an output file of our choosing (see [Graphviz Output Formats](https://graphviz.org/docs/outputs/)) using for example:
```python
memory_graph.render(data, "my_graph.pdf")
memory_graph.render(data, "my_graph.png")
memory_graph.render(data, "my_graph.gv") # Graphviz DOT file
```


## Python Data Model ##
The [Python Data Model](https://docs.python.org/3/reference/datamodel.html) makes a distiction between immutable and mutable types:

* **immutable**: bool, int, float, complex, str, tuple, bytes, frozenset
* **mutable**: list, dict, set, class, ... (all other types)


### immutable type ###
In the code below variable `a` and `b` both reference the same `int` value 10. An `int` is an immutable type and therefore when we change variable `a` its value can **not** be mutated in place, and thus a copy is made and `a` and `b` reference a different value afterwards.
```python
import memory_graph
memory_graph.rewrite_to_node.reduce_reference_children.remove("int") # shows references to 'int'

a = 10
b = a
memory_graph.render(locals(), 'immutable1.png')
a += 1
memory_graph.render(locals(), 'immutable2.png')
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/immutable1.png)
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/immutable2.png)


### mutable type ###
With mutable types the result is different. In the code below variable `a` and `b` both reference the same `list` value [4, 3, 2]. A `list` is a mutable type and therefore when we change variable `a` its value **can** be mutated in place and thus `a` and `b` both reference the same new value afterwards. Thus changing `a` also changes `b` and vice versa. Sometimes we want this but other times we don't and then we will have to make a copy so that `b` is independent from `a`.
```python
import memory_graph

a = [4, 3, 2]
b = a
memory_graph.render(locals(), 'mutable1.png')
a.append(1)
memory_graph.render(locals(), 'mutable2.png')
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/mutable1.png)
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/mutable2.png)

Python makes this distiction between mutable and immutable types because a value of a mutable type generally could be large and therefore it would be slow to make a copy each time we change it. On the other hand, a value of a changable immutable type generally is small and therefore fast to copy.


### copying ###
Python offers three different "copy" options that we will demonstrate using a nested list:

```python
import memory_graph
import copy

a = [ [1, 2], ['x', 'y'] ] # a nested list (a list containing other lists)

# three different ways to make a "copy" of 'a':
c1 = a
c2 = copy.copy(a) # equivalent to:   a.copy() a[:] list(a)
c3 = copy.deepcopy(a)

memory_graph.show(locals())
```

* `c1` is an **assignment**, all the data is shared, nothing is copied
* `c2` is a **shallow copy**, only the data referenced by the first reference is copied and the underlying data is shared
* `c3` is a **deep copy**, all the data is copied, nothing is shared

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/copies.png)


### custom copy method ###
We can write our own custom copy function or method in case the three "copy" options don't do what we want. For example the copy() method of My_Class in the code below copies the `numbers` but shares the `letters` between the two objects.
```python
import memory_graph
import copy

class My_Class:

    def __init__(self):
        self.numbers = [1, 2]
        self.letters = ['x', 'y']

    def copy(self): # custom copy method copies the numbers but shares the letters
        c = copy.copy(self)
        c.numbers = copy.copy(self.numbers)
        return c

a = My_Class()
b = a.copy()

memory_graph.show(locals())
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/copy_method.png)


## Debugging ##
Often it is useful to graph all the local variables using:
```python
memory_graph.show(locals(), block=True)
```

So much so that function `d()` is available as alias for this for easier debugging. Additionally it logs all local variables by printing them which helps comparing them over time. For example:
```python
from memory_graph import d

my_squares = []
my_squares_ref = my_squares
for i in range(5):
    my_squares.append(i**2)
    d()
my_squares_copy = my_squares.copy()
d()
```
which after pressing ENTER a number of times results in:

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example2.png)
```
my_squares: [0, 1, 4, 9, 16]
my_squares_ref: [0, 1, 4, 9, 16]
i: 4
my_squares_copy: [0, 1, 4, 9, 16]
```

Function `d()` has these default arguments:
```python
def d(data=None, log=True, graph=True, block=True):
```
- data: the data that is handled, defaults to `locals()`
- log: if True the data is printed
- graph: if True the data is visualized as a graph
- block: if True the function blocks until the ENTER key is pressed

To print to a log file instead of standard output use:
```python
memory_graph.log_file = open("log_file.txt", "w")
```

### Watchpoint in Debugger ###
Alternative you can also set this expression as a 'watchpoint' in a debugger tool and open the "my_debug_graph.pdf" output file for a continuous visualization of all the local variables while debugging:
```
memory_graph.render(locals(), "my_debug_graph.pdf")
```
This avoids having to add any memory_graph `show()` or `d()` calls to your code.


## Call Stack ##
Function ```memory_graph.get_call_stack()``` returns the full call stack that holds for each called function all the local variables. This enables us to visualize the local variables of each of the called functions on the stack simultaneously. This helps to visualize if variables of different called functions share any data between them. Here for example we call function ```add_one()``` with arguments ```a, b, c``` and add one to change each of them.

```python
import memory_graph

def add_one(a, b, c):
    a += 1
    b.append(1)
    c.append(1)
    memory_graph.show(memory_graph.get_call_stack())

a = 10
b = [4, 3, 2]
c = [4, 3, 2]

add_one(a, b, c.copy())
print(f"a:{a} b:{b} c:{c}")
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/add_one.png)

As ```a``` is of immutable type 'int' and as we call the function with a copy of ```c``` the visualization shows only ```b``` is shared so only ```b``` is changed in the calling stack frame as reflected in the printed output:
```
a:0 b:[4, 3, 2, 1] c:[4, 3, 2]
```

### recursion ###
The call stack also helps to visualize how recursion works. Here we show each step of how recursively ```factorial(3)``` is computed:

```python
import memory_graph

def factorial(n):
    if n==0:
        return 1
    memory_graph.show( memory_graph.get_call_stack(), block=True )
    result = n * factorial(n-1)
    memory_graph.show( memory_graph.get_call_stack(), block=True )
    return result

factorial(3)
```
  <div><img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/factorial1.png" /></div>
  <div><img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/factorial2.png" /></div>
  <div><img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/factorial3.png" /></div>
  <div><img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/factorial4.png" /></div>
  <div><img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/factorial5.png" /></div>
  <div><img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/factorial6.png" /></div>
and the final result is: 1 x 2 x 3 = 6

### Call Stack in Watchpoint ###
The ```memory_graph.get_call_stack()``` doesn't work well in a watchpoint context in most debuggers because debuggers introduce additional stack frames that cause problems. Use these alternative functions for various debuggers to ignore the problematic stack frames:

| debugger | function |
|:---|:---|
| **pdb, pudb** | `memory_graph.get_call_stack_pdb()` |
| **Visual Studio Code** | `memory_graph.get_call_stack_vscode()` |
| **Pycharm** | `memory_graph.get_call_stack_pycharm()` |

#### Other Debuggers ####
For other debuggers, invoke this function within the watchpoint context. Then, in the "call_stack.txt" file, identify and select the names of the functions you wish to include in the call stack, specifically those 'after' and 'up_to' your point of interest.
```
memory_graph.save_call_stack("call_stack.txt")
```
and then call this function to get the desired call stack to render:
```
memory_graph.get_call_stack_after_up_to(after_function, up_to_function="<module>")
```


## Datastructure Examples ##
Module memory_graph can be very useful in a course about datastructures, some examples:

### Doubly Linked List ###
```python
import memory_graph
import random
random.seed(0) # use same random numbers each run

class Node:

    def __init__(self, value):
        self.prev = None
        self.value = value
        self.next = None

class LinkedList:

    def __init__(self):
        self.head = None
        self.tail = None

    def add_front(self, value):
        new_node = Node(value)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

linked_list = LinkedList()
n = 100
for i in range(n):
    new_value = random.randrange(n)
    linked_list.add_front(new_value)
    memory_graph.show(locals(), block=True) # <--- draw linked list
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/linked_list.png)

### Binary Tree ###
```python
import memory_graph
import random
random.seed(0) # use same random numbers each run

class Node:

    def __init__(self, value):
        self.smaller = None
        self.value = value
        self.larger = None

class BinTree:

    def __init__(self):
        self.root = None

    def add_recursive(self, new_value, node):
        memory_graph.show(locals(), block=True) # <--- draw tree when adding recursively
        if new_value < node.value:
            if node.smaller is None:
                node.smaller = Node(new_value)
            else:
                self.add_recursive(new_value, node.smaller)
        else:
            if node.larger is None:
                node.larger = Node(new_value)
            else:
                self.add_recursive(new_value, node.larger)

    def add(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            self.add_recursive(value, self.root)

tree = BinTree()
n = 100
for i in range(n):
    new_value = random.randrange(100)
    tree.add(new_value)
    memory_graph.show(locals(), block=True)  # <--- draw tree after adding
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/bin_tree.png)

### Hash Set ###
```python
import memory_graph
import random
random.seed(0) # use same random numbers each run

class HashSet:

    def __init__(self, capacity=20):
        self.buckets = [None] * capacity

    def add(self, value):
        index = hash(value) % len(self.buckets)
        if self.buckets[index] is None:
            self.buckets[index] = [value]
        else:
            self.buckets[index].append(value)

    def contains(self, value):
        index = hash(value) % len(self.buckets)
        if self.buckets[index] is None:
            return False
        return value in self.buckets[index]

    def remove(self, value):
        index = hash(value) % len(self.buckets)
        if self.buckets[index] is not None:
            self.buckets[index].remove(value)
        
hash_set = HashSet()
n = 100
for i in range(n):
    new_value = random.randrange(n)
    hash_set.add(new_value)
    memory_graph.show(locals(), block=True) # <--- draw hash set
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/hash_set.png)


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
  - custom accessor functions to define how to read various data types


### Config Examples ###
This example shows a class with a class variable and has some recursive references.
```python
import memory_graph
my_list = [10, 20, 10]

class My_Class:
    my_class_var = 20 # class variable
    
    def __init__(self):
        self.var1 = "foo"
        self.var2 = "bar"
        self.var3 = 20

obj1 = My_Class()
obj2 = My_Class()

data=[my_list, my_list, obj1, obj2]

my_list.append(data)
my_list.append(my_list) # recursive reference

memory_graph.show(locals())
```
![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example3.png)

With configuration:
```
memory_graph.graphviz_nodes.linear_layout_vertical = False           # draw lists,tuples,sets,... horizontally
memory_graph.graphviz_nodes.category_to_color_map['list'] = 'yellow' # change color of 'list' type
memory_graph.graphviz_nodes.spacing = 15                             # more spacing in each node
memory_graph.graphviz_nodes.graph_attr['ranksep'] = '1.2'            # more vertical separation
memory_graph.graphviz_nodes.graph_attr['nodesep'] = '1.2'            # more horizontal separation
memory_graph.rewrite_to_node.reduce_reference_children.remove("int") # draw references to 'int' type
```

this example looks like:

![image](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/example4.png)


### Custom Accessor Functions ###
For any type a custom accessor function can be introduced. For example Pandas DataFrames and Series are not visualized correctly by default. This can be fixed by adding custom accessor functions:
```python
import memory_graph
import pandas as pd

data = {'Name'   : [ 'Tom', 'Anna', 'Steve', 'Lisa'],
        'Age'    : [    28,     34,      29,     42],
        'Length' : [  1.70,   1.66,    1.82,   1.73] }
df = pd.DataFrame(data)

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
- In Jupyter Notebooks `locals()` has additional variables that cause problems, use `memory_graph.locals_jupyter()` to filter these out. Use `memory_graph.get_call_stack_jupyter()` to filter these out of the whole calls stack.

- When graph edges overlap it can be hard to distinguish them. Using an interactive graphviz viewer, such as [xdot](https://github.com/jrfonseca/xdot.py), on a '*.gv' DOT output file will help.


## Author ##
Bas Terwijn


## Inspiration ##
Inspired by [Python Tutor](https://pythontutor.com/).
