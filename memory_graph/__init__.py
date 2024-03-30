from memory_graph.Memory_Graph import Memory_Graph

import memory_graph.config_default as config_default
import memory_graph.utils as utils

import inspect
import sys

__version__ = "0.1.26"
__author__ = 'Bas Terwijn'

log_file=sys.stdout
press_enter_text="press <ENTER> to continue..."

def get_source_location(stack_index):
    frameInfo = inspect.stack()[stack_index] # get frameInfo of calling frame
    filename= frameInfo.filename
    line_nr= frameInfo.lineno
    function = frameInfo.function
    return f'in file:"{filename}" line:{line_nr} function:"{function}"'

def get_locals_from_calling_frame(stack_index):
    frameInfo = inspect.stack()[stack_index] # get frameInfo of calling frame
    return frameInfo.frame.f_locals

def create_graph(data):
    memory_graph = Memory_Graph(data)
    return memory_graph.get_graph()

def show(data,block=False):
    graph = create_graph(data)
    #print('graph:',graph)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', {get_source_location(2)}, {press_enter_text}")

def render(data, output_filename=None, block=False):
    graph = create_graph(data)
    filename = output_filename if output_filename else graph.filename
    graph.render(outfile=filename)
    if block:
        input(f"rendering '{filename}', {get_source_location(2)}, {press_enter_text}")

def to_str(data):
    try:
        return str(data)
    except Exception as e:
        return f"problem printing: {type(data)}"

def d(data=None,log=False,graph=True,block=True,stack_index=2):
    if data is None:
        data=get_locals_from_calling_frame(stack_index)
    if graph:
        grph=create_graph(data)
        grph.view()
    if log:
        print(f"debugging, {get_source_location(stack_index)}",file=log_file)
        if isinstance(data,dict):
            for key,value in utils.filter_dict_attributes(data.items()):
                print(f"{to_str(key)}: {to_str(value)}", file=log_file, flush=True)
        else:
            print(to_str(data), file=log_file, flush=True)
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

def get_call_stack_after_up_to(after_function,up_to_function="<module>"):
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

def locals_jupyter(stack_index=2):
    return jupyter_locals_filter(get_locals_from_calling_frame(stack_index))

def get_call_stack_jupyter(up_to_function="<module>",stack_index=2):
    call_stack = get_call_stack(up_to_function,stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = jupyter_locals_filter(call_stack[globals_frame])
    return call_stack
