from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import graphviz_nodes

import inspect
import sys

__version__ = "0.1.26"
__author__ = 'Bas Terwijn'

log_file=sys.stdout
press_enter_text="press <ENTER> to continue..."

def get_source_location(stack_index=3):
    try:
        frameInfo = inspect.stack()[-stack_index] # get frameInfo of calling frame
        filename= frameInfo.filenamepop
        line_nr= frameInfo.lineno
        function = frameInfo.function
        return f'in file:"{filename}" line:{line_nr} function:"{function}"'
    except Exception as e:
        #print("Exception:",e)
        pass
    return ""

def get_locals_from_calling_frame(stack_index=3):
    frameInfo = inspect.stack()[-stack_index] # get frameInfo of calling frame
    return frameInfo.frame.f_locals

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

def to_str(data):
    try:
        return str(data)
    except Exception as e:
        return f"problem printing: {type(data)}"

def d(data=None,log=True,graph=True,block=True,stack_index=3):
    if data is None:
        data=get_locals_from_calling_frame(stack_index)
    if log:
        print(f"debugging, {get_source_location()}",file=log_file)
        if rewrite.is_dict_type(data):
            for key,value in rewrite.filter_dict(data):
                print(f"{to_str(key)}: {to_str(value)}",file=log_file)
        else:
            print(to_str(data),file=log_file)
        print("",end='',file=log_file,flush=True)
    if graph:
        grph=create_graph(data)
        grph.view()
    if block:
        input(press_enter_text)

# ------------ call stack

def take_up_to(condition,iterable):
    for i in iterable:
        yield i
        if condition(i):
            return

def take_after(condition,iterable):
    taking = False
    for i in iterable:
        if taking:
            yield i
        if condition(i):
            taking = True

def stack_frames_to_dict(frames):
    return {f"{level}: {frameInfo.function}" : frameInfo.frame.f_locals
            for level, frameInfo in enumerate(frames)}

def get_call_stack(up_to_function="<module>",stack_index=1):
    frames = reversed(list(
        take_up_to(lambda i: i.function==up_to_function, inspect.stack()[stack_index:])
        ))
    return stack_frames_to_dict(frames)

def get_call_stack_after_up_to(after_function, up_to_function="<module>"):
    frames = reversed(list(
            take_up_to(lambda i: i.function == up_to_function,
            take_after(lambda i: i.function == after_function, inspect.stack()))
            ))
    return stack_frames_to_dict(frames)

def get_call_stack_pdb(after_function="trace_dispatch",up_to_function="<module>"):
    return get_call_stack_after_up_to(after_function,up_to_function)

def get_call_stack_vscode(after_function="do_wait_suspend",up_to_function="<module>"):
    return get_call_stack_after_up_to(after_function,up_to_function)

def get_call_stack_pycharm(after_function="trace_dispatch",up_to_function="<module>"):
    return get_call_stack_after_up_to(after_function,up_to_function)

def save_call_stack(filename):
    with open(filename,'w') as file:
        for f in inspect.stack():
            file.write(f"function:{f.function} filename:{f.filename}\n")

# ------------ jupyter filtering
            
jupyter_filter_keys = {'exit','quit','v','In','Out','jupyter_filter_keys'}
def jupyter_locals_filter(jupyter_locals):
    return {k:v for k,v in jupyter_locals.items()
            if k not in jupyter_filter_keys and k[0] != '_'}

def locals_jupyter(stack_index=3):
    return jupyter_locals_filter(get_locals_from_calling_frame(stack_index))

def get_call_stack_jupyter(up_to_function="<module>",stack_index=2):
    call_stack = get_call_stack(up_to_function,stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = jupyter_locals_filter(call_stack[globals_frame])
    return call_stack
