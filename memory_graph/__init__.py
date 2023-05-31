from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import graphviz_nodes

import traceback
import inspect
import sys

__version__ = "0.1.15"
__author__ = 'Bas Terwijn'

def block_print():
    press="press <ENTER> to continue..."
    try:
        iterable=traceback.walk_stack(None)
        iterator=iter(iterable)
        next(iterator) # skip frame 
        frame,linenr=next(iterator) # read the frame that called show()/render()
        tb=inspect.getframeinfo(frame)
        return f'in file:"{tb.filename}" line:{tb.lineno} function:"{tb.function}", '+press
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

def get_locals_from_calling_frame():
    iterable=traceback.walk_stack(None)
    iterator=iter(iterable)
    next(iterator) # skip frame
    frame,linenr=next(iterator) # read the frame that called d()
    return frame.f_locals # get locals() from the calling frame
            
def d(data=None,log=True,stream=sys.stdout,graph=True,block=True):
    prompt_line=f"debugging, {block_print()}"
    if data is None:
        data=get_locals_from_calling_frame()
    if log:
        if rewrite.is_dict_type(data):
            for key in data:
                if not type(key) is str or not rewrite.is_dunder_name(key):
                    if not rewrite.is_ignore_type(key):
                        value=data[key]
                        if not rewrite.is_ignore_type(value):
                            print(f"{key}: {value}",file=stream)
        else:
            print(data,file=stream)
        if not stream==sys.stdout:
            print(prompt_line,file=stream,flush=True)
    if graph:
        grph=create_graph(data)
        grph.view()
    if block:
        if stream==sys.stdout:
            input(prompt_line)
        else:
            input()
