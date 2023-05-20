from types import NoneType
from types import MappingProxyType
import graphviz

from memory_graph import Node
from memory_graph import rewrite

layout_vertical=False
type_category_to_color_map={
    "NoneType":"gray", "type":"lime", "bool":"pink", "int":"green", "float":"yellow", "str":"cyan", # fundamental types
    "tuple":"orange", "list":"brown1", "set":"darkolivegreen1", "frozenset":"darkolivegreen3", "dict":"blue", "mappingproxy":"blue3", "class":"purple" # containers
}
uncategorized_color="red"

def type_category_to_color(type_catergory):
    if type_catergory in type_category_to_color_map:
        return type_category_to_color_map[type_catergory]
    return uncategorized_color

def get_type_name(node):
    return rewrite.get_name_attribute(node.get_type())

def get_type_category(node):
    if rewrite.is_class_type(node.get_original_data()):
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
                                         }))
    if len(label)>0 and label[-1]=='>': # workaround, weird problem if label ends with '>'
        label+=" "
    return label

def get_element_label(element):
    value=element.get_value()
    if value is None:
        return ""
    return add_escape_chars(str(value))

def build_label_line(node):
    label=" | ".join( (f"<f{index}> "+ get_element_label(element) for index,element in enumerate(node.get_elements())) )
    if layout_vertical:
        return "{ "+label+" }"
    return label

def build_label_key_value(node):
    keys=   " | ".join( (f"<f{index}> "+ get_element_label(element) for index,element in enumerate(node.get_elements()) if index%2==0) ) 
    values= " | ".join( (f"<f{index}> "+ get_element_label(element) for index,element in enumerate(node.get_elements()) if index%2==1) ) 
    return f"{{ {keys} }} | {{ {values} }}"
    
def get_node_label(node):
    if rewrite.is_dict_type(node.get_original_data()) or rewrite.is_class_type(node.get_original_data()):
        return build_label_key_value(node)
    return build_label_line(node)

def get_refs(node,all_nodes):
    return ((f"{get_node_name(node)}:f{index}",f"{get_node_name(all_nodes[element.get_ref()])}")
            for index,element in enumerate(node.get_elements())
            if not element.get_ref() is None)

def create_node(node,all_nodes,graph):
    name="node"+str(node.get_index())
    node_label=get_node_label(node)
    type_name=get_type_name(node)
    color=type_category_to_color(get_type_category(node))
    if node.get_index()==0:
        graph.node(name, node_label, xlabel=type_name, style="filled", fillcolor=color, penwidth="3")
    else:
        graph.node(name, node_label, xlabel=type_name, style="filled", fillcolor=color)
    for node_src,node_dst in get_refs(node,all_nodes):
        graph.edge(node_src, node_dst)
    
def create_graph_recursive(all_nodes,node_index,memo,graph):
    if not node_index in memo:
        memo.add(node_index)
        node=all_nodes[node_index]
        create_node(node,all_nodes,graph)
        for e in node.get_elements():
            ref=e.get_ref()
            if ref:
                create_graph_recursive(all_nodes,ref,memo,graph)

def create_graph(all_nodes):
    graph=graphviz.Digraph('memory_graph', node_attr={'shape': 'record'})
    create_graph_recursive(all_nodes,0,set(),graph)
    return graph
