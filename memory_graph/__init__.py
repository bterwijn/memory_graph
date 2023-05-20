from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import graphviz_nodes

__version__ = "0.1.2"
__author__ = 'Bas Terwijn'

def create_graph(data):
    all_nodes=rewrite_to_node.rewrite_data(data)
    return graphviz_nodes.create_graph(all_nodes)

def show(data,block=True):
    graph=create_graph(data)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', press <ENTER> to continue...")

def render(data,output_filename=None,block=True):
    graph=create_graph(data)
    if output_filename:
        graph.render(outfile=output_filename)
        if block:
            input(f"rendering '{output_filename}', press <ENTER> to continue...")
    else:
        graph.render()
        if block:
            input(f"rendering '{graph.filename}', press <ENTER> to continue...")

def filter(dictionary):
    filtered_dict={}
    for key in dictionary:
        value=dictionary[key]
        if rewrite.is_known_type(key) and rewrite.is_known_type(value):
            if type(key)==str:
                if rewrite.is_dunder_name(key):
                    continue
                if key in {'memory_graph'}:
                    continue
            filtered_dict[key]=value
    return filtered_dict
