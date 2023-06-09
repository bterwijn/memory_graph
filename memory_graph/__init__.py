from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import graphviz_nodes

import traceback
import inspect
import sys

__version__ = "0.1.16"
__author__ = 'Bas Terwijn'

log_file=sys.stdout
press_enter_text="press <ENTER> to continue..."

def get_source_location():
    try:
        iterable=traceback.walk_stack(None)
        iterator=iter(iterable)
        next(iterator) # skip frame 
        frame,linenr=next(iterator) # read the frame that called show()/render()
        tb=inspect.getframeinfo(frame)
        return f'in file:"{tb.filename}" line:{tb.lineno} function:"{tb.function}"'
    except Exception as e:
        #print("Exception:",e)
        pass
    return ""

def create_graph(data):
    all_nodes=rewrite_to_node.rewrite_data(data)
    return graphviz_nodes.create_graph(all_nodes)

def show(data,block=False):
    graph=create_graph(data)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', {get_source_location()}, {press_enter_text}")

def render(data,output_filename=None,block=False):
    graph=create_graph(data)
    if output_filename:
        graph.render(outfile=output_filename)
        if block:
            input(f"rendering '{output_filename}', {get_source_location()}, {press_enter_text}")
    else:
        graph.render()
        if block:
            input(f"rendering '{graph.filename}', {get_source_location()}, {press_enter_text}")

def get_locals_from_calling_frame():
    iterable=traceback.walk_stack(None)
    iterator=iter(iterable)
    next(iterator) # skip frame
    frame,linenr=next(iterator) # read the frame that called d()
    return frame.f_locals # get locals() from the calling frame
            
def d(data=None,log=True,graph=True,block=True):
    if data is None:
        data=get_locals_from_calling_frame()
    if log:
        print(f"debugging, {get_source_location()}",file=log_file)
        if rewrite.is_dict_type(data):
            for key,value in rewrite.filter_dict(data):
                print(f"{key}: {value}",file=log_file)
        else:
            print(data,file=log_file)
        print("",end='',file=log_file,flush=True)
    if graph:
        grph=create_graph(data)
        grph.view()
    if block:
        input(press_enter_text)
