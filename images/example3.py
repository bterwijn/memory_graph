import memory_graph

memory_graph.graphviz_nodes.layout_vertical = False                       # draw lists,tuples,sets,... horizontally
memory_graph.graphviz_nodes.type_category_to_color_map['list'] = 'yellow' # change color of 'list' types
memory_graph.rewrite_to_node.reduce_reference_types.remove(int)           # draw references to 'int' types

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

memory_graph.render( locals(), 'example3.png' )
