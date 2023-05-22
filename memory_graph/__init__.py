from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import graphviz_nodes

__version__ = "0.1.7"
__author__ = 'Bas Terwijn'

def create_graph(data):
    all_nodes=rewrite_to_node.rewrite_data(data)
    return graphviz_nodes.create_graph(all_nodes)

def show(data,block=False):
    graph=create_graph(data)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', press <ENTER> to continue...")

def render(data,output_filename=None,block=False):
    graph=create_graph(data)
    if output_filename:
        graph.render(outfile=output_filename)
        if block:
            input(f"rendering '{output_filename}', press <ENTER> to continue...")
    else:
        graph.render()
        if block:
            input(f"rendering '{graph.filename}', press <ENTER> to continue...")
