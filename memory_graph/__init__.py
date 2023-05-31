from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import graphviz_nodes

import traceback
import inspect

__version__ = "0.1.15"
__author__ = 'Bas Terwijn'

def block_print(skipframes):
    press="press <ENTER> to continue..."
    try:
        iterable=traceback.walk_stack(None)
        iterator=iter(iterable)
        for i in range(skipframes):
            next(iterator) # pop frame 
        frame,linenr=next(iterator) # read the frame that called show()/render()
        tb=inspect.getframeinfo(frame)
        return f'from file:"{tb.filename}" line:{tb.lineno} function:"{tb.function}", '+press
    except:
        pass
    return s

def create_graph(data):
    all_nodes=rewrite_to_node.rewrite_data(data)
    return graphviz_nodes.create_graph(all_nodes)

def show(data,block=False,skipframes=1):
    graph=create_graph(data)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', {block_print(skipframes)}")

def render(data,output_filename=None,block=False,skipframes=1):
    graph=create_graph(data)
    if output_filename:
        graph.render(outfile=output_filename)
        if block:
            input(f"rendering '{output_filename}', {block_print(skipframes)}")
    else:
        graph.render()
        if block:
            input(f"rendering '{graph.filename}', {block_print(skipframes)}")

def d(data=None,block=True):
    if data is None:
        iterable=traceback.walk_stack(None)
        iterator=iter(iterable)
        frame,linenr=next(iterator) # read the frame that called d()
        data=frame.f_locals # get locals() from the calling frame
    show(data,block=block,skipframes=2)
