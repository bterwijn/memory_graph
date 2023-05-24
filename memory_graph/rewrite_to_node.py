from types import MappingProxyType

from memory_graph import rewrite
from memory_graph import Node

reduce_reference_parents={"category_class"}
reduce_reference_children={"bool", "int", "float", "complex", "str", "range", "bytes"}

def is_reduce_reference(parent,child):
    return ( child.get_type_name()  in reduce_reference_children or
             child.get_category()   in reduce_reference_children or
             parent.get_type_name() in reduce_reference_parents  or
             parent.get_category()  in reduce_reference_parents )

def my_construct_singular(data,category):
    node=Node.Node(data,category)
    node.add_element(Node.Element(value=data))
    return node

def my_construct_iterable(data,category):
    return Node.Node(data,category,category=="category_dict")
    
def my_add_to_iterable(iterable,data):
    if is_reduce_reference(iterable,data):
        iterable.add_elements(data)
    else:
        iterable.add_element(data.get_ref())

rewrite.construct_singular_fun=my_construct_singular
rewrite.construct_iterable_fun=my_construct_iterable
rewrite.add_to_iterable_fun=my_add_to_iterable

def rewrite_data(data):
    Node.all_nodes=[]
    Node.Node.index=0
    rewrite.rewrite_data(data)
    return Node.all_nodes
