from types import MappingProxyType
import graphviz

from memory_graph import Node
from memory_graph import rewrite

linear_layout_vertical=True
linear_any_ref_layout_vertical=False
linear_all_ref_layout_vertical=False
key_value_layout_vertical=True
key_value_any_ref_layout_vertical=False
key_value_all_ref_layout_vertical=False
padding=0
spacing=5
join_references_count=5
join_circle_size="0.4"
join_circle_minlen="2"
max_string_length=70
category_to_color_map={
    "NoneType":"gray", "type":"lightgreen", "bool":"pink", "int":"green", "float":"yellow", "str":"cyan", # fundamental types
    "tuple":"orange", "list":"lightcoral", "set":"darkolivegreen1", "frozenset":"darkolivegreen3", "dict":"royalblue1", "mappingproxy":"royalblue2", # containers
    "category_class":"orchid", "category_custom":"seagreen1" # catergories
}
uncategorized_color="red"
graph_attr={}
node_attr={'shape':'plaintext'}
edge_attr={}

# ------- private ----------
taken_children=set()
graphviz_nodes=[]
graphviz_references={}


def add_reference(src,dst):
    if not dst in graphviz_references:
        graphviz_references[dst]=[]
    graphviz_references[dst].append(src)

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

def limit_string(s):
    if len(s)>max_string_length:
        return s[:max_string_length]+"..."
    return s

def get_element_label(element):
    value=element.get_value()
    if value is None:
        return ""
    return avoid_html_injection(limit_string(str(value)))

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
    return f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> </TD></TR></TABLE>>'
    
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
    return f'<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X"> </TD></TR></TABLE>>'
    
def get_node_label(node,border=1):
    if node.is_key_value():
        return build_label_key_value(node,border)
    return build_label_linear(node,border)

def get_refs(node,all_nodes):
    return ((f"{get_node_name(node)}:f{index}",f"{get_node_name(all_nodes[element.get_ref()])}:X")
            for index,element in enumerate(node.get_elements())
            if not element.get_ref() is None)

def traverse_node(node,all_nodes,graph):
    #name="node"+str(node.get_index())
    #border=2 if node.get_index()==0 else 1
    #node_label=get_node_label(node,border)
    #graph.node(name, node_label, xlabel=node.get_type_name())
    graphviz_nodes.append(node)
    my_children=[]
    for node_src,node_dst in get_refs(node,all_nodes):
        add_reference(node_src,node_dst)
        if not node_dst in taken_children:
            taken_children.add(node_dst)
            my_children.append(node_dst)
    if len(my_children)>1:
        lineup=" -> ".join(my_children)
        graph.body.append('{ rank="same"  '+lineup+'  [weight=99,style=invis]; }\n')
        
def traverse_graph_recursive(all_nodes,node_index,memo,graph):
    if not node_index in memo:
        memo.add(node_index)
        node=all_nodes[node_index]
        for e in node.get_elements():
            ref=e.get_ref()
            if ref:
                traverse_graph_recursive(all_nodes,ref,memo,graph)
        traverse_node(node,all_nodes,graph) # create while backtracking recursion

def add_graphviz_nodes(graph):
    graphviz_nodes.sort(key=lambda n : n.get_index())
    for node in graphviz_nodes:
        name=get_node_name(node)
        border=2 if node.get_index()==0 else 1
        node_label=get_node_label(node,border)
        graph.node(name, node_label, xlabel=node.get_type_name())
        
def add_graphviz_references(graph):
    for dst in graphviz_references:
        src_list=graphviz_references[dst]
        if len(src_list)<join_references_count:
            for src in src_list:
                graph.edge(src, dst)
        else:
            join="join_"+dst[:dst.index(':')]
            graph.node(join, label="", height=join_circle_size, width=join_circle_size, shape="circle", weight="50")
            graph.edge(join, dst)
            for src in src_list:
                graph.edge(src, join, dir="none", minlen=join_circle_minlen)
            
def create_graph(all_nodes):
    taken_children.clear()
    graphviz_nodes.clear()
    graphviz_references.clear()
    #Node.print_all_nodes(all_nodes)
    graph=graphviz.Digraph('memory_graph',
                           graph_attr=graph_attr,
                           node_attr=node_attr,
                           edge_attr=edge_attr)
    traverse_graph_recursive(all_nodes,0,set(),graph)
    add_graphviz_nodes(graph)
    add_graphviz_references(graph)
    return graph
