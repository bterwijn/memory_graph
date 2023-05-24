from types import MappingProxyType
import graphviz

from memory_graph import Node
from memory_graph import rewrite

linear_layout_vertical=True
linear_any_ref_layout_vertical=False
linear_all_ref_layout_vertical=False
key_value_layout_vertical=True
key_value_any_ref_layout_vertical=True
key_value_all_ref_layout_vertical=False
category_to_color_map={
    "NoneType":"gray", "type":"lightgreen", "bool":"pink", "int":"green", "float":"yellow", "str":"cyan", # fundamental types
    "tuple":"orange", "list":"lightcoral", "set":"darkolivegreen1", "frozenset":"darkolivegreen3", "dict":"royalblue1", "mappingproxy":"royalblue2", # containers
    "category_class":"orchid" # catergories
}
key_color="cornsilk"
uncategorized_color="red"
padding=0
spacing=5
empty_label=""
graph_attr={}
node_attr={'shape':'plaintext'}
edge_attr={}


taken_children=set()

def get_color(node):
    category=node.get_type_name()
    if category in category_to_color_map:
        return category_to_color_map[category]
    category=node.get_category()
    if category in category_to_color_map:
        return category_to_color_map[category]
    return uncategorized_color

def get_node_name(node):
    return "node"+str(node.get_index())

def avoid_html_injection(label):
    label=label.translate(str.maketrans({"<" : r"&lt;",
                                         ">" : r"&gt;",
                                         "&" : r"&amp;",
                                         "\"": r"&quot;",
                                         "\'": r"&apos;",
                                         }))
    return label

def get_element_label(element):
    value=element.get_value()
    if value is None:
        return empty_label
    return avoid_html_injection(str(value))

def test_references_linear(node,fun):
    return fun((not e.get_ref() is None) for e in node.get_elements())

def test_references_key_value(node,fun):
    return fun((not e.get_ref() is None) for i,e in enumerate(node.get_elements()) if i%2==1)

def build_label_linear(node,border):
    color=get_color(node)
    vertical=linear_layout_vertical
    if test_references_linear(node,any):
        vertical&=linear_any_ref_layout_vertical
    if test_references_linear(node,all):
        vertical&=linear_all_ref_layout_vertical
    if len(node.get_elements())>0:
        if vertical:
            cells="".join( (f'<TR><TD PORT="f{index}"> {get_element_label(element)} </TD></TR>' for index,element in enumerate(node.get_elements())) )
        else:
            cells="<TR>"+ "".join( (f'<TD PORT="f{index}"> {get_element_label(element)} </TD>' for index,element in enumerate(node.get_elements())) ) +"</TR>"
        table=f'<TABLE BORDER="{border}" CELLSPACING="{spacing}" CELLPADDING="{padding}">{cells}</TABLE>'
        return f'<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> {table} </TD></TR></TABLE>>'
    return f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> {empty_label} </TD></TR></TABLE>>'
    
def build_label_key_value(node,border):
    color=get_color(node)
    vertical=key_value_layout_vertical
    if test_references_key_value(node,any):
        vertical&=key_value_any_ref_layout_vertical
    if test_references_key_value(node,all):
        vertical&=key_value_all_ref_layout_vertical
    if len(node.get_elements())>0:
        iterator=iter(enumerate(node.get_elements()))
        if vertical:
            cells=""
            while True:
                try:
                    ki,k=next(iterator)
                    vi,v=next(iterator)
                    cells+=f'<TR><TD PORT="f{ki}" STYLE="ROUNDED"> {get_element_label(k)} </TD><TD PORT="f{vi}"> {get_element_label(v)} </TD></TR>'
                except StopIteration:
                    break
            table=f'<TABLE BORDER="{border}" CELLSPACING="{spacing}" CELLPADDING="{padding}" BGCOLOR="{color}">{cells}</TABLE>'
        else:
            keys='<TR>'
            values='<TR>'
            while True:
                try:
                    ki,k=next(iterator)
                    keys+=f'<TD PORT="f{ki}" STYLE="ROUNDED"> {get_element_label(k)} </TD>'
                    vi,v=next(iterator)
                    values+=f'<TD PORT="f{vi}"> {get_element_label(v)} </TD>'
                except StopIteration:
                    break
            keys+='</TR>'
            values+='</TR>'
            table=f'<TABLE BORDER="{border}" CELLSPACING="{spacing}" CELLPADDING="{padding}" BGCOLOR="{color}">{keys}{values}</TABLE>'
        return f'<<TABLE BORDER="0" CELLSPACING="0" CELLPADDING="0"><TR><TD PORT="X"> {table} </TD></TR></TABLE>>'
    return f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> {empty_label} </TD></TR></TABLE>>'
    
def get_node_label(node,border=1):
    if node.is_key_value():
        return build_label_key_value(node,border)
    return build_label_linear(node,border)

def get_refs(node,all_nodes):
    return ((f"{get_node_name(node)}:f{index}",f"{get_node_name(all_nodes[element.get_ref()])}:X")
            for index,element in enumerate(node.get_elements())
            if not element.get_ref() is None)

def create_node(node,all_nodes,graph):
    name="node"+str(node.get_index())
    border=2 if node.get_index()==0 else 1
    node_label=get_node_label(node,border)
    graph.node(name, node_label, xlabel=node.get_type_name())
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
    #Node.print_all_nodes(all_nodes)
    graph=graphviz.Digraph('memory_graph',
                           graph_attr=graph_attr,
                           node_attr=node_attr,
                           edge_attr=edge_attr)
    create_graph_recursive(all_nodes,0,set(),graph)
    return graph
