from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import graphviz_nodes

import traceback
import inspect

__version__ = "0.1.14"
__author__ = 'Bas Terwijn'

def block_print():
    press="press <ENTER> to continue..."
    try:
        iterable=traceback.walk_stack(None)
        iterator=iter(iterable)
        next(iterator) # skip frame
        frame,linenr=next(iterator) # read the frame that called show()/render()
        tb=inspect.getframeinfo(frame)
        return f'from file:"{tb.filename}" line:{tb.lineno} function:"{tb.function}", '+press
    except:
        pass
    return s

def create_graph(data):
    all_nodes=rewrite_to_node.rewrite_data(data)
    return graphviz_nodes.create_graph(all_nodes)

def show(data,block=False):
    graph=create_graph(data)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', {block_print()}")

def render(data,output_filename=None,block=False):
    graph=create_graph(data)
    if output_filename:
        graph.render(outfile=output_filename)
        if block:
            input(f"rendering '{output_filename}', {block_print()}")
    else:
        graph.render()
        if block:
            input(f"rendering '{graph.filename}', {block_print()}")
