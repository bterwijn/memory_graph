from types import NoneType
from types import MappingProxyType

from memory_graph import rewrite
from memory_graph import Node

reduce_reference_types={NoneType, bool, int, float, complex, str, range, bytes}
reduce_references_for_classes=True

def is_duplication_type(value):
    return type(value) in reduce_reference_types

def my_construct_singular(data):
    node=Node.Node(data)
    node.add_element(Node.Element(value=data))
    return node

def my_construct_iterable(data):
    return Node.Node(data)
    
def my_add_to_iterable(iterable,data):
    if is_duplication_type(data.get_original_data()):
        iterable.add_elements(data.get_elements())
    elif reduce_references_for_classes and rewrite.is_type_with_dict(iterable.get_original_data()):
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
    return Node.all_nodes
