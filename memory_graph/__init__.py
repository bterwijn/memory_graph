from memory_graph.Memory_Graph import Memory_Graph

import memory_graph.config_default as config_default
import memory_graph.utils as utils

import inspect
import sys

__version__ = "0.2.00"
__author__ = 'Bas Terwijn'

log_file=sys.stdout
press_enter_text="press <ENTER> to continue..."

def get_source_location(stack_index):
    """ Helper function to get the source location of the stack with 'stack_index' of the call stack. """
    frameInfo = inspect.stack()[stack_index] # get frameInfo of calling frame
    filename= frameInfo.filename
    line_nr= frameInfo.lineno
    function = frameInfo.function
    return f'in {filename}:{line_nr} function:"{function}"'

def get_locals_from_calling_frame(stack_index):
    """ Helper function to get locals of the stack with 'stack_inex' of the call stack. """
    frameInfo = inspect.stack()[stack_index] # get frameInfo of calling frame
    return frameInfo.frame.f_locals

def create_graph(data,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Creates and returns a memory graph from 'data'. """
    memory_graph = Memory_Graph(data, colors, vertical_orientations, slicers)
    return memory_graph.get_graph()

def show(data,block=False,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Shows the graph of 'data' and optionally blocks. """
    graph = create_graph(data, colors, vertical_orientations, slicers)
    #print('graph:',graph)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', {get_source_location(2)}, {press_enter_text}")

def render(data, output_filename=None, block=False,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Renders the graph of 'data' to 'output_filename' and optionally blocks. """
    graph = create_graph(data, colors, vertical_orientations, slicers)
    filename = output_filename if output_filename else graph.filename
    graph.render(outfile=filename)
    if block:
        input(f"rendering '{filename}', {get_source_location(2)}, {press_enter_text}")

def to_str(data):
    try:
        return str(data)
    except Exception as e:
        return f"problem printing: {type(data)}"

def d(data=None,graph=True,log=False,block=True,stack_index=2,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ 
    Shows the graph of and optionally prints 'data', and optionally blocks.
    When no 'data' is given, the locals of the calling frame are used as 'data'.
    """
    if data is None:
        data=get_locals_from_calling_frame(stack_index)
    if graph:
        grph=create_graph(data, colors, vertical_orientations, slicers)
        grph.view()
    if log:
        if isinstance(data,dict):
            for key,value in utils.filter_dict_attributes(data.items()):
                print(f"{to_str(key)}: {to_str(value)}", file=log_file, flush=True)
        else:
            print(to_str(data), file=log_file, flush=True)
        if not block and not log_file == sys.stdout:
            print(f"debugging, {get_source_location(stack_index)}",file=log_file)
    if block:
        input(f"debugging, {get_source_location(stack_index)}, {press_enter_text}")

# ------------ call stack

def stack_frames_to_dict(frames):
    """ Returns a dictionary representing the data on the call stack. 
    Each key is the stack level and function name, each value is the locals of the frame at that level. 
    """
    return {f"{level}: {frameInfo.function}" : frameInfo.frame.f_locals
            for level, frameInfo in enumerate(frames)}

def get_call_stack(up_to_function="<module>",stack_index=1):
    """ Gets the call stack up to the function 'up_to_function'. """
    frames = reversed(list(
        utils.take_up_to(lambda i: i.function==up_to_function, inspect.stack()[stack_index:])
        ))
    return stack_frames_to_dict(frames)

def get_call_stack_after_up_to(after_function,up_to_function="<module>"):
    """ Gets the call stack after the function 'after_function' up to the function 'up_to_function'."""
    frames = reversed(list(
            utils.take_up_to(lambda i: i.function == up_to_function,
            utils.take_after(lambda i: i.function == after_function, inspect.stack()))
            ))
    return stack_frames_to_dict(frames)

def get_call_stack_pdb(after_function="trace_dispatch",up_to_function="<module>"):
    """ Get the call stack in a 'pdb' debugger session, filtering out the 'pdb' functions that polute the graph. """
    return get_call_stack_after_up_to(after_function,up_to_function)

def get_call_stack_vscode(after_function="do_wait_suspend",up_to_function="<module>"):
    """ Get the call stack in a 'vscode' debugger session, filtering out the 'vscode' functions that polute the graph. """
    return get_call_stack_after_up_to(after_function,up_to_function)

def get_call_stack_pycharm(after_function="trace_dispatch",up_to_function="<module>"):
    """ Get the call stack in a 'pycharm' debugger session, filtering out the 'pycharm' functions that polute the graph. """
    return get_call_stack_after_up_to(after_function,up_to_function)

def save_call_stack(filename):
    """ Save the call stack to 'filename' for inspection to see what functions need to be 
    filtered out to create the desired graph. """
    with open(filename,'w') as file:
        for f in inspect.stack():
            file.write(f"function:{f.function} filename:{f.filename}\n")

# ------------ jupyter filtering
            
jupyter_filter_keys = {'exit','quit','v','In','Out','jupyter_filter_keys'}
def jupyter_locals_filter(jupyter_locals):
    """ Filter out the jupyter specific keys that polute the graph. """
    return {k:v for k,v in jupyter_locals.items()
            if k not in jupyter_filter_keys and k[0] != '_'}

def locals_jupyter(stack_index=2):
    """ Get the locals of the calling frame in a jupyter notebook, filtering out the jupyter specific keys. """
    return jupyter_locals_filter(get_locals_from_calling_frame(stack_index))

def get_call_stack_jupyter(up_to_function="<module>",stack_index=2):
    """ Get the call stack in a jupyter notebook, filtering out the jupyter specific keys. """
    call_stack = get_call_stack(up_to_function,stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = jupyter_locals_filter(call_stack[globals_frame])
    return call_stack
