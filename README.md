# Installation #
Install (or upgrade) `memory_graph` using pip:
```
pip install --upgrade memory_graph
```
Additionally [Graphviz](https://graphviz.org/download/) needs to be installed.

# Sharing Data #

In Python, assigning the list from variable `a` to variable `b` causes both variables to reference the same list object and therefore share the data. Consequently, any change applied through one variable will impact the other. This behavior can lead to elusive bugs if a programmer incorrectly assumes that list `a` and `b` are independent.

<table><tr><td> 

```python
import memory_graph as mg

# create the lists 'a' and 'b'
a = [4, 3, 2]
b = a
a.append(1) # changing 'a' changes 'b'

# print the 'a' and 'b' list
print('a:', a)
print('b:', b)

# check if 'a' and 'b' share data
print('ids:', id(a), id(b))
print('identical?:', a is b)

# show all local variables in a graph
mg.show( locals() )
```

</td><td>

![mutable2.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/mutable2.png)

a graph showing `a` and `b` share data

</td></tr></table>

The fact that `a` and `b` share data can not be verified by printing the lists. It can be verified by comparing the identity of both variables using the `id()` function or by using the `is` comparison operator as shown in the program output below, but this quickly becomes impractical for larger programs. 
```{verbatim}
a: 4, 3, 2, 1
b: 4, 3, 2, 1
ids: 126432214913216 126432214913216
identical?: True
```
A better way to understand what data is shared is to draw a graph of the data using the [memory_graph](https://pypi.org/project/memory-graph/) package.

# Memory Graph #
The [memory_graph](https://pypi.org/project/memory-graph/) package can graph many different data types.

```python
import memory_graph as mg

class MyClass:

    def __init__(self, x, y):
        self.x = x
        self.y = y

data = [ range(1, 2), (3, 4), {5, 6}, {7:'seven', 8:'eight'},  MyClass(9, 10) ]
mg.show(data, block=True)
```
![many_types.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/many_types.png)

By using `block=True` the program blocks until the &lt;Enter&gt; key is pressed so you can view the graph before continuing program execution (and possibly viewing later graphs). Instead of showing the graph you can also render it to an output file of your choosing (see [Graphviz Output Formats](https://graphviz.org/docs/outputs/)) using for example:

```python
mg.render(data, "my_graph.pdf")
mg.render(data, "my_graph.png")
mg.render(data, "my_graph.gv") # Graphviz DOT file
```

# Chapters #

[1. Python Data Model](#1-python-data-model)

[2. Debugging](#2-debugging)

[3. Call Stack](#3-call-stack)

[4. Datastructure Examples](#4-datastructure-examples)

[5. Configuration](#5-configuration)

[6. Extensions](#6-extensions)

[7. Jupyter Notebook](#7-jupyter-notebook)

[8. Troubleshooting](#8-troubleshooting)


## Author ##
Bas Terwijn

## Inspiration ##
Inspired by [Python Tutor](https://pythontutor.com/).

## Supported by ##
<img src="https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/uva.png" alt="University of Amsterdam" width="600">

___
___

## 1. Python Data Model ##
The [Python Data Model](https://docs.python.org/3/reference/datamodel.html) makes a distiction between immutable and mutable types:

* **immutable**: bool, int, float, complex, str, tuple, bytes, frozenset
* **mutable**: list, set, dict, classes, ... (most other types)


### Immutable Type ###
In the code below variable `a` and `b` both reference the same tuple value (4, 3, 2). A tuple is an immutable type and therefore when we change variable `a` its value **cannot** be mutated in place, and thus a copy is made and `a` and `b` reference a different value afterwards.

```python
import memory_graph as mg

a = (4, 3, 2)
b = a
mg.render(locals(), 'immutable1.png')
a += (1,)
mg.render(locals(), 'immutable2.png')
```
| ![mutable1.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/immutable1.png) | ![mutable2.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/immutable2.png) |
|:-----------------------------------------------------------:|:-------------------------------------------------------------:|
| immutable1.png | immutable2.png |


### Mutable Type ###
With mutable types the result is different. In the code below variable `a` and `b` both reference the same `list` value [4, 3, 2]. A `list` is a mutable type and therefore when we change variable `a` its value **can** be mutated in place and thus `a` and `b` both reference the same new value afterwards. Thus changing `a` also changes `b` and vice versa. Sometimes we want this but other times we don't and then we will have to make a copy so that `b` is independent from `a`.

```python
import memory_graph as mg

a = [4, 3, 2]
b = a
mg.render(locals(), 'mutable1.png')
a += [1] # equivalent to:  a.append(1)
mg.render(locals(), 'mutable2.png')
```
| ![mutable1.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/mutable1.png) | ![mutable2.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/mutable2.png) |
|:-----------------------------------------------------------:|:-------------------------------------------------------------:|
| mutable1.png | mutable2.png |

One practical reason why Python makes the distinction between mutable and immutable types is that a value of a mutable type could be large, making it inefficient to copy each time we change it. Immutable values generally don't need to change as much or are smaller, which makes copying less of a concern.

### Copying ###
Python offers three different "copy" options that we will demonstrate using a nested list:

```python
import memory_graph as mg
import copy

a = [ [1, 2], ['x', 'y'] ] # a nested list (a list containing lists)

# three different ways to make a "copy" of 'a':
c1 = a
c2 = copy.copy(a) # equivalent to:  a.copy() a[:] list(a)
c3 = copy.deepcopy(a)

mg.show(locals())
```

* `c1` is an **assignment**, nothing is copied, all the values are shared
* `c2` is a **shallow copy**, only the value referenced by the first reference is copied, all the underlying values are shared
* `c3` is a **deep copy**, all the values are copied, nothing is shared

![copies.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/copies.png)


### Custom Copy Method ###
We can write our own custom copy function or method in case the three "copy" options don't do what we want. For example the copy() method of My_Class in the code below copies the `digits` but shares the `letters` between the two objects.

```python
import memory_graph as mg
import copy

class My_Class:

    def __init__(self):
        self.digits = [1, 2]
        self.letters = ['x', 'y']

    def copy(self): # custom copy method copies the digits but shares the letters
        c = copy.copy(self)
        c.digits = copy.copy(self.digits)
        return c

a = My_Class()
b = a.copy()

mg.show(locals())
```
![copy_method.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/copy_method.png)


## 2. Debugging ##
Often it is useful to graph all the local variables using:
```python
mg.show(locals(), block=True)
```

So much so that function `d()` is available as alias for this for easier debugging. Additionally it can optionally log the data by printing them. For example:
```python
import memory_graph as mg

squares = []
squares_collector = []
for i in range(1,6):
    squares.append(i**2)
    squares_collector.append(squares.copy())
    mg.d(log=True)
```
which after pressing &lt;Enter&gt; a number of times results in:

![debugging.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/debugging.gif)
```
squares: [1, 4, 9, 16, 25]
squares_collector: [[1], [1, 4], [1, 4, 9], [1, 4, 9, 16], [1, 4, 9, 16, 25]]
i: 5
```

Function `d()` has these default arguments:
```python
def d(data=None, graph=True, log=False, block=True):
```
- data: the data that is handled, defaults to `locals()` when not specified
- graph: if True the data is visualized as a graph
- log: if True the data is printed
- block: if True the function blocks until the &lt;Enter&gt; key is pressed

To print to a log file instead of standard output use:
```python
mg.log_file = open("my_log_file.txt", "w")
```

### Watch in Debugger ###
Alternatively you get an even better debugging experience when you set expression:
```
mg.render(locals(), "my_debug_graph.pdf")
```
as a *watch* in a debugger tool and open the "my_debug_graph.pdf" output file. This continuouly shows the graph of all the local variables while debugging and avoids having to add any memory_graph `show()`, `render()`, or `d()` calls to your code.


## 3. Call Stack ##
The function `mg.get_call_stack()` returns the complete call stack, including all local variables for each function in the stack. This allows us to simultaneously visualize the local variables of all the called functions. By doing so, we can identify whether any local variables from different functions in the call stack share data with one another. Here for example we call function ```add_one()``` with arguments ```a, b, c``` that adds 1 to each of its arguments.

```python
import memory_graph as mg

def add_one(a, b, c):
    a += [1]
    b += (1,)
    c += [1]
    mg.show(mg.get_call_stack())

a = [4, 3, 2]
b = (4, 3, 2)
c = [4, 3, 2]

add_one(a, b, c.copy())
print(f"a:{a} b:{b} c:{c}")
```
![add_one.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/add_one.png)

In the printed output only `a` is changed as a result of the function call:
```
a:[4, 3, 2, 1] b:(4, 3, 2) c:[4, 3, 2]
```

This is because `b` is of immutable type 'tuple' so its value gets copied automatically when it is changed. And because the function is called with a copy of `c`, its original value is not changed by the function. The value of variable `a` is the only value of mutable type that is shared between the root stack frame **'0: \<module>'** and the **'1: add_one'** stack frame of the function so only that variable is affected as a result of the function call. The other changes remain confined to the local variables of the ```add_one()``` function.


### Recursion ###
The call stack can be used to visualize how recursion works. Here we show each step of how recursively ```factorial(3)``` is computed:

```python
import memory_graph as mg

def factorial(n):
    if n==0:
        return 1
    mg.show( mg.get_call_stack(), block=True )
    result = n * factorial(n-1)
    mg.show( mg.get_call_stack(), block=True )
    return result

print(factorial(3))
```

Execution results in:

![factorial.gif](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/factorial.gif)

and the result is: 1 x 2 x 3 = 6

### Power Set ###
A more insteresting recursive example that shows sharing of data is power_set(). A power set is the set of all subsets of a collection of values.

```python
import memory_graph as mg

def get_subsets(subsets, data, i, subset):
    mg.show(mg.get_call_stack(), block=True)
    if i == len(data):
        subsets.append(subset.copy())
        return
    subset.append(data[i])
    get_subsets(subsets, data, i+1, subset) #    do include data[i]
    subset.pop()
    get_subsets(subsets, data, i+1, subset) # don't include data[i]
    mg.show(mg.get_call_stack(), block=True)

def power_set(data):
    subsets = []
    get_subsets(subsets, data, 0, [])
    return subsets

print( power_set(['a', 'b', 'c']) )
```

Execution results in:

![power_set.gif](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/power_set.gif)
```
[['a', 'b', 'c'], ['a', 'b'], ['a', 'c'], ['a'], ['b', 'c'], ['b'], ['c'], []]
```


### Call Stack in Watch Context ###
The ```mg.get_call_stack()``` doesn't work well in a *watch* context in most debuggers because debuggers introduce additional stack frames that cause problems. Use these alternative functions for various debuggers to filter out these problematic stack frames:

| debugger | function to get the call stack |
|:---|:---|
| **pdb, pudb** | `mg.get_call_stack_pdb()` |
| **Visual Studio Code** | `mg.get_call_stack_vscode()` |
| **Pycharm** | `mg.get_call_stack_pycharm()` |

#### Other Debuggers ####
For other debuggers, invoke this function within the *watch* context. Then, in the "call_stack.txt" file, identify the slice of functions you wish to include in the call stack.
```
mg.save_call_stack("call_stack.txt")
```
Choose 'after' and 'up_to' what function you want to slice and then call this function to get the desired call stack:
```
mg.get_call_stack_after_up_to(after_function, up_to_function="<module>")
```


## 4. Datastructure Examples ##
Module memory_graph can be very useful in a course about datastructures, some examples:

### Doubly Linked List ###
```python
import memory_graph as mg
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
        mg.show(locals(), block=True) # <--- draw graph

linked_list = LinkedList()
n = 100
for i in range(n):
    new_value = random.randrange(n)
    linked_list.add_front(new_value)
```
![linked_list.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/linked_list.png)

### Binary Tree ###
```python
import memory_graph as mg
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
        mg.show(locals(), block=True) # <--- draw graph

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
```
![bin_tree.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/bin_tree.png)

### Hash Set ###
```python
import memory_graph as mg
import random
random.seed(0) # use same random numbers each run

class HashSet:

    def __init__(self, capacity=15):
        self.buckets = [None] * capacity

    def add(self, value):
        index = hash(value) % len(self.buckets)
        if self.buckets[index] is None:
            self.buckets[index] = []
        bucket = self.buckets[index]
        bucket.append(value)
        mg.show(locals(), block=True) # <--- draw graph

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
```
![hash_set.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/hash_set.png)


## 5. Configuration ##
Different aspects of memory_graph can be configured. The default configuration is reset by importing 'mg.config_default'.

- ***mg.config.max_number_nodes*** : int
  - The maxium number of Nodes shown in the graph. When the graph gets too big set this to a smaller number. A `★` symbol indictes where the graph is cut short.

- ***mg.config.max_string_length*** : int
  - The maximum length of strings shown in the graph. Longer strings will be truncated.

- ***mg.config.not_node_types*** : set
  - Holds all types for which no seperate node is drawn but that instead are shown as elements in their parent Node.

- ***mg.config.no_child_references_types*** : set
  - The set of key_value types that don't draw references to their direct childeren but have their children shown as elements of their node.

- ***mg.config.type_to_node*** : dict
  - Determines how a data types is converted to a Node (sub)class for visualization in the graph.

- ***mg.config.type_to_color*** : dict
  - Maps each type to the [graphviz color](https://graphviz.org/doc/info/colors.html) it gets in the graph. 

- ***mg.config.type_to_vertical_orientation*** : dict
  - Maps each type to its orientation. Use 'True' for vertical and 'False' for horizontal. If not specified Node_Linear and Node_Key_Value are vertical unless they have references to children.

- ***mg.config.type_to_slicer*** : dict
  - Maps each type to a Slicer. A slicer determines how many elements of a data type are shown in the graph to prevent the graph from getting too big. 'Slicer()' does no slicing, 'Slicer(1,2,3)' shows just 1 element at the beginning, 2 in the middle, and 3 at the end.

### Temporary Configuration ###
In addition to the global configuration, a temporary configuration can be set for a single `show()`, `render()`, or `d()` call to change the colors, orientation, and slicer. This example highlights a particular list element in red, gives it a horizontal orientation, and overwrites the default slicer for lists:

```python
import memory_graph as mg

data = [ list(range(20)) for i in range(1,5)]
highlight = data[2]

mg.show( locals(),
    colors                = {id(highlight): "red"      }, # set color to "red"
    vertical_orientations = {id(highlight): False      }, # set horizontal orientation
    slicers               = {id(highlight): mg.Slicer()}  # set no slicing 
)
```
![highlight.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/highlight.png)

## 6. Extensions ##
Different extensions are available for types from other Python packages. 

### Numpy ###
Numpy types `arrray` and `matrix` and `ndarray` can be graphed with the "memory_graph.extension_numpy" extension:

```python
import memory_graph as mg
import numpy as np
import memory_graph.extension_numpy
np.random.seed(0) # use same random numbers each run

array = np.array([1.1, 2, 3, 4, 5])
matrix = np.matrix([[i*20+j for j in range(20)] for i in range(20)])
ndarray = np.random.rand(20,20)
mg.show(locals(), block=True)
```
![extension_numpy.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/extension_numpy.png)

### Pandas ###
Pandas types `Series` and `DataFrame` can be graphed with the "memory_graph.extension_pandas" extension:

```python
import memory_graph as mg
import pandas as pd
import memory_graph.extension_pandas

series = pd.Series( [i for i in range(20)] )
dataframe1 = pd.DataFrame({  "calories": [420, 380, 390],
                             "duration": [50, 40, 45] })
dataframe2 = pd.DataFrame({  'Name'   : [ 'Tom', 'Anna', 'Steve', 'Lisa'],
                             'Age'    : [    28,     34,      29,     42],
                             'Length' : [  1.70,   1.66,    1.82,   1.73] },
                            index=['one', 'two', 'three', 'four']) # with row names
mg.show(locals(), block=True)
```
![extension_pandas.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/extension_pandas.png)

## 7. Jupyter Notebook ##

In Jupyter Notebook `locals()` has additional variables that cause problems in the graph, use `mg.locals_jupyter()` to get the local variables with these problematic variables filtered out. Use `mg.get_call_stack_jupyter()` to get the whole call stack with these variables filtered out. 

See for example [jupyter_example.ipynb](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/jupyter_example.ipynb).
![jupyter_example.png](https://raw.githubusercontent.com/bterwijn/memory_graph/main/images/jupyter_example.png)


## 8. Troubleshooting ##

- Adobe Acrobat Reader [doesn't refresh a PDF file](https://superuser.com/questions/337011/windows-pdf-viewer-that-auto-refreshes-pdf-when-compiling-with-pdflatex) when it changes on disk and blocks updates which results in an `Could not open 'somefile.pdf' for writing : Permission denied` error. One solution is to install a PDF reader that does refresh ([Evince](https://www.fosshub.com/Evince.html) for example) and set it as the default PDF reader. Another solution is to `render()` the graph to a different output format and open it manually.

- When graph edges overlap it can be hard to distinguish them. Using an interactive graphviz viewer, such as [xdot](https://github.com/jrfonseca/xdot.py), on a '*.gv' DOT output file will help.

