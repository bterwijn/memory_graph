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

my_list.append(data)
my_list.append(my_list) # recursive reference

import memory_graph
memory_graph.graphviz_nodes.linear_layout_vertical = False           # draw lists,tuples,sets,... horizontally
memory_graph.graphviz_nodes.category_to_color_map['list'] = 'yellow' # change color of 'list' type
memory_graph.graphviz_nodes.spacing=15                               # more spacing in each node
memory_graph.graphviz_nodes.graph_attr['ranksep']='1.2'              # more vertical separation
memory_graph.graphviz_nodes.graph_attr['nodesep']='1.2'              # more horizontal separation
memory_graph.rewrite_to_node.reduce_reference_children.remove("int") # draw references to 'int' type
memory_graph.render( locals(), 'example4.png' )
