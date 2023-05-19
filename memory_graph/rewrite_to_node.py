from types import NoneType
from types import MappingProxyType

from memory_graph import rewrite
from memory_graph import Node

reduce_references=True

def is_duplication_type(value):
    return type(value) in {NoneType, bool, int, float, str, complex, range, bytes}

def my_construct_singular(data):
    node=Node.Node(data)
    node.add_element(Node.Element(value=data))
    return node

def my_construct_iterable(data):
    return Node.Node(data)
    
def my_add_to_iterable(iterable,data):
    if not reduce_references:
        iterable.add_element(data.get_ref())
    else:
        if is_duplication_type(data.get_original_data()):
            iterable.add_elements(data.get_elements())
        elif rewrite.is_class_type(iterable.get_original_data()):
            if type(data.get_original_data()) is MappingProxyType:
                iterable.add_element(Node.Element(value="class vars:"))
                iterable.add_element(data.get_ref())
            else:
                iterable.add_elements(data.get_elements())
        else:
            iterable.add_element(data.get_ref())

rewrite.construct_singular_fun=my_construct_singular
rewrite.construct_iterable_fun=my_construct_iterable
rewrite.add_to_iterable_fun=my_add_to_iterable

def rewrite_data(data):
    Node.all_nodes=[]
    Node.Node.index=0
    rewrite.rewrite_data(data)
    #Node.print_all_nodes(Node.all_nodes)
    return Node.all_nodes
