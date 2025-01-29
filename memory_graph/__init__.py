# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph.memory_to_nodes as memory_to_nodes
import memory_graph.config as config
import memory_graph.config_default
import memory_graph.config_helpers as config_helper
import memory_graph.utils as utils

import inspect
import sys

import graphviz

__version__ = "0.3.09"
__author__ = 'Bas Terwijn'
render_filename = 'memory_graph.pdf'
block_shows_location = True
press_enter_message = "Press <Enter> to continue..."

def get_source_location(stack_index):
    """ Helper function to get the source location of the stack with 'stack_index' of the call stack. """
    frameInfo = inspect.stack()[stack_index] # get frameInfo of calling frame
    filename= frameInfo.filename
    line_nr= frameInfo.lineno
    function = frameInfo.function
    return f'{filename}:{line_nr} function:"{function}"'

def block(fun=None, *args, **kwargs):
    """
    Calls the given function `fun` with specified arguments and keyword arguments,
    waits for the user to press Enter, and returns the result of `fun`.
    """
    if 'stack_index' in kwargs:
        stack_index = kwargs['stack_index']
        del kwargs['stack_index']
    result = None
    if callable(fun):
        result = fun(*args, **kwargs)
    if memory_graph.block_shows_location:
        print('blocked at ' + get_source_location(stack_index), end=', ')
    if memory_graph.press_enter_message:
        print(memory_graph.press_enter_message)
    input()
    return result

def block_deprecated_message():
    print("Warning: 'block=True' deprecated, use mg.block(fun) instead.")
    input(f"{get_source_location(3)}, Press <Enter> to continue...")

def create_graph(data,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Creates and returns a memory graph from 'data'. """
    config_helper.set_config(colors, vertical_orientations, slicers)
    graphviz_graph = memory_to_nodes.memory_to_nodes(data)
    return graphviz_graph

def show(data ,block=False,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Shows the graph of 'data' and optionally blocks. """
    graph = create_graph(data, colors, vertical_orientations, slicers)
    graph.view()
    if block:
        block_deprecated_message()

def render(data, outfile=None, block=False,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Renders the graph of 'data' to 'outfile' and optionally blocks. """
    if outfile is None:
        outfile = memory_graph.render_filename
    graph = create_graph(data, colors, vertical_orientations, slicers)
    graph.render(outfile=outfile)
    if block:
        block_deprecated_message()

# ------------ aliases

def sl(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_calling_frame(stack_index=stack_index)
    memory_graph.show(data, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def ss(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.get_call_stack() and blocks. 
    """
    data = get_call_stack(stack_index=stack_index)
    memory_graph.show(data, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def bsl(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_calling_frame(stack_index=stack_index)
    memory_graph.block(memory_graph.show, data, stack_index=stack_index+1, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def bss(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.get_call_stack() and blocks. 
    """
    data = get_call_stack(stack_index=stack_index)
    memory_graph.block(memory_graph.show, data, stack_index=stack_index+1, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def rl(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_calling_frame(stack_index=stack_index)
    memory_graph.render(data, block=False, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def rs(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.get_call_stack() and blocks. 
    """
    data = get_call_stack(stack_index=stack_index)
    memory_graph.render(data, block=False, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def brl(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_calling_frame(stack_index=stack_index)
    memory_graph.block(memory_graph.render, data, stack_index=stack_index+1, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def brs(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.get_call_stack() and blocks. 
    """
    data = get_call_stack(stack_index=stack_index)
    memory_graph.block(memory_graph.render, data, stack_index=stack_index+1, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def l(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    bsl(stack_index=stack_index+1, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def s(stack_index=2, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.get_call_stack() and blocks. 
    """
    bss(stack_index=stack_index+1, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)


# ------------ call stack

def get_locals_from_calling_frame(stack_index=1):
    """ Helper function to get locals of the stack with 'stack_inex' of the call stack. """
    frameInfo = inspect.stack()[stack_index] # get frameInfo of calling frame
    return frameInfo.frame.f_locals

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
