from types import NoneType
from types import MappingProxyType
import graphviz

from memory_graph import Node
from memory_graph import rewrite

layout_vertical=True
type_category_to_color_map={
    "NoneType":"gray", "type":"lime", "bool":"pink", "int":"green", "float":"yellow", "str":"cyan", # fundamental types
    "tuple":"orange", "list":"brown1", "set":"darkolivegreen1", "frozenset":"darkolivegreen3", "dict":"royalblue1", "mappingproxy":"royalblue3", "class":"orchid" # containers
}
uncategorized_color="red"
padding=0
spacing=3


taken_children=set()

def type_category_to_color(type_catergory):
    if type_catergory in type_category_to_color_map:
        return type_category_to_color_map[type_catergory]
    return uncategorized_color

def get_type_name(node):
    return rewrite.get_name_attribute(node.get_type())

def get_type_category(node):
    if rewrite.is_type_with_dict(node.get_original_data()):
        return "class"
    return get_type_name(node)

def get_node_name(node):
    return "node"+str(node.get_index())

def add_escape_chars(label):
    label=label.translate(str.maketrans({"<":  r"\<",
                                         ">":  r"\>",
                                         "|":  r"\|",
                                         "{":  r"\{",
                                         "}":  r"\}",
                                         })) # TODO
    return label

def get_element_label(element):
    value=element.get_value()
    if value is None:
        return "&nbsp;"
    return add_escape_chars(str(value))

def build_label_line(node,border=1):
    color=type_category_to_color(get_type_category(node))
    if len(node.get_elements())>0:
        if layout_vertical:
            cells="".join( (f'<TR><TD PORT="f{index}"> {get_element_label(element)} </TD></TR>' for index,element in enumerate(node.get_elements())) )
        else:
            cells="<TR>"+ "".join( (f'<TD PORT="f{index}">{get_element_label(element)}</TD>' for index,element in enumerate(node.get_elements())) ) +"</TR>"
        table=f'<TABLE BORDER="{border}" CELLSPACING="{spacing}" CELLPADDING="{padding}">{cells}</TABLE>'
        return f'<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> {table} </TD></TR></TABLE>>'
    return f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> &nbsp; </TD></TR></TABLE>>'
    
def build_label_key_value(node,border=1):
    color=type_category_to_color(get_type_category(node))
    if len(node.get_elements())>0:
        iterator=iter(enumerate(node.get_elements()))
        cells=""
        while True:
            try:
                ki,k=next(iterator)
                vi,v=next(iterator)
                cells+=f'<TR><TD PORT="f{ki}"> {get_element_label(k)} </TD><TD PORT="f{vi}"> {get_element_label(v)} </TD></TR>'
            except StopIteration:
                break
            table=f'<TABLE BORDER="{border}" CELLSPACING="{spacing}" CELLPADDING="{padding}" BGCOLOR="{color}">{cells}</TABLE>'
        return f'<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0"><TR><TD PORT="X"> {table} </TD></TR></TABLE>>'
    return f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> &nbsp; </TD></TR></TABLE>>'
    
def get_node_label(node,border=1):
    if rewrite.is_dict_type(node.get_original_data()) or rewrite.is_type_with_dict(node.get_original_data()):
        return build_label_key_value(node,border)
    return build_label_line(node,border)

def get_refs(node,all_nodes):
    return ((f"{get_node_name(node)}:f{index}",f"{get_node_name(all_nodes[element.get_ref()])}:X")
            for index,element in enumerate(node.get_elements())
            if not element.get_ref() is None)

def create_node(node,all_nodes,graph):
    name="node"+str(node.get_index())
    border=2 if node.get_index()==0 else 1
    node_label=get_node_label(node,border)
    type_name=get_type_name(node)
    color=type_category_to_color(get_type_category(node))
    graph.node(name, node_label, xlabel=type_name)
    my_children=[]
    for node_src,node_dst in get_refs(node,all_nodes):
        if node_dst in taken_children:
            graph.edge(node_src, node_dst, weight='0')
        else:
            graph.edge(node_src, node_dst)
            taken_children.add(node_dst)
            my_children.append(node_dst)
    if len(my_children)>1:
        lineup=" -> ".join(my_children)
        graph.body.append("{ rank=same  "+lineup+"  [weight=99,style=invis]; }\n")
    
def create_graph_recursive(all_nodes,node_index,memo,graph):
    if not node_index in memo:
        memo.add(node_index)
        node=all_nodes[node_index]
        for e in node.get_elements():
            ref=e.get_ref()
            if ref:
                create_graph_recursive(all_nodes,ref,memo,graph)
        create_node(node,all_nodes,graph) # create while backtracking recursion 

def create_graph(all_nodes):
    global taken_children
    taken_children=set()
    graph=graphviz.Digraph('memory_graph', graph_attr={'concentrate':'true'}, node_attr={'shape':'none', 'margin':'0'})
    create_graph_recursive(all_nodes,0,set(),graph)
    return graph
