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
from memory_graph.call_stack import call_stack

import graphviz

__version__ = "0.3.22"
__author__ = 'Bas Terwijn'
render_filename = 'memory_graph.pdf'
last_show_filename = None
block_prints_location = True
press_enter_message = "Press <Enter> to continue..."

def get_source_location(stack_index=0):
    """ Helper function to get the source location of the stack with 'stack_index' of the call stack. """
    frameInfo = inspect.stack()[1+stack_index] # get frameInfo of calling frame
    filename= frameInfo.filename
    line_nr= frameInfo.lineno
    function = frameInfo.function
    return f'{filename}:{line_nr} function:"{function}"'

def block(fun=None, *args, **kwargs):
    """
    Calls the given function `fun` with specified arguments and keyword arguments,
    waits for the user to press Enter, and returns the result of `fun`.
    """
    stack_index = 0
    if 'stack_index' in kwargs:
        stack_index = kwargs['stack_index']
        del kwargs['stack_index']
    result = None
    if callable(fun):
        result = fun(*args, **kwargs)
    if memory_graph.block_prints_location:
        print('blocked at ' + get_source_location(1+stack_index), end=', ')
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

def render(data, outfile=None, view=False, block=False,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Renders the graph of 'data' to 'outfile' or `memory_graph.render_filename` when not specified. """
    if outfile is None:
        outfile = memory_graph.render_filename
    graph = create_graph(data, colors, vertical_orientations, slicers)
    if outfile.endswith('.gv') or outfile.endswith('.dot'):
        graph.save(filename=outfile)
    else:
        graph.render(outfile=outfile, view=view, cleanup=False, quiet=False, quiet_view=False)
    if block:
        block_deprecated_message()

def show(data, outfile=None, view=False, block=False,
                 colors = None,
                 vertical_orientations = None,
                 slicers = None):
    """ Shows the graph of 'data' by first rendering and then opening the default viewer
    application by file extension at first call, when the outfile changes, or
    when view is True. """
    if outfile is None:
        outfile = memory_graph.render_filename
    open_view = (outfile != memory_graph.last_show_filename) or view
    render(data=data, outfile=outfile, view=open_view, block=block,
           colors=colors,
           vertical_orientations=vertical_orientations,
           slicers=slicers)
    memory_graph.last_show_filename = outfile

    
# ------------ aliases

def sl(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.show(data, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def ss(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.show(data, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def bsl(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.show, data, stack_index=1+stack_index, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def bss(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.show, data, stack_index=1+stack_index, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def rl(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.render(data, block=False, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def rs(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.render(data, block=False, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def brl(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.render, data, stack_index=1+stack_index, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def brs(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.render, data, stack_index=1+stack_index, block=False, 
                       colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)

def l(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of locals() and blocks. 
    """
    bsl(stack_index=1+stack_index, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)
    
def s(stack_index=0, colors = None, vertical_orientations = None, slicers = None):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    bss(stack_index=1+stack_index, colors=colors, vertical_orientations=vertical_orientations, slicers=slicers)


# ------------ call stack

def get_locals_from_call_stack(stack_index=0):
    """ Helper function to get locals of the stack with 'stack_inex' of the call stack. """
    frameInfo = inspect.stack()[1+stack_index] # get frameInfo of calling frame
    return frameInfo.frame.f_locals

def get_function_name(frameInfo):
    frame = frameInfo.frame
    func_name = frame.f_code.co_name
    if 'self' in frame.f_locals:  # instance method
        return f"{frame.f_locals['self'].__class__.__name__}.{func_name}"
    elif 'cls' in frame.f_locals:  # class method
        return f"{frame.f_locals['cls'].__name__}.{func_name}"
    else:  # forget about static method, too complex
        return func_name  # just the function

def stack_frames_to_dict(frames):
    """ Returns a dictionary representing the data on the call stack. 
    Each key is the stack level and function name, each value is the locals of the frame at that level. 
    """
    def to_dict(value): #  fix by TerenceTux for Python 3.13
        return {k: v for k, v in value.items()}
    return call_stack({f"{level}: {get_function_name(frameInfo)}" : to_dict(frameInfo.frame.f_locals)
            for level, frameInfo in enumerate(frames)})

def locals():
    """ Returns local variables. """
    return locals()

def stack(up_to_function="<module>",stack_index=0):
    return get_call_stack(up_to_function, 1+stack_index)
def get_call_stack(up_to_function="<module>",stack_index=0):
    """ Gets the call stack up to the function 'up_to_function'. """
    frames = reversed(list(
        utils.take_up_to(lambda i: i.function==up_to_function, inspect.stack()[1+stack_index:])
        ))
    return stack_frames_to_dict(frames)

def stack_after_up_to(after_function,up_to_function="<module>"):
    return get_call_stack_after_up_to(after_function, up_to_function)
def get_call_stack_after_up_to(after_function,up_to_function="<module>"):
    """ Gets the call stack after the function 'after_function' up to the function 'up_to_function'."""
    frames = reversed(list(
            utils.take_up_to(lambda i: i.function == up_to_function,
            utils.take_after(lambda i: i.function == after_function, inspect.stack()))
            ))
    return stack_frames_to_dict(frames)

def stack_pdb(after_function="trace_dispatch",up_to_function="<module>"):
    return get_call_stack_pdb(after_function, up_to_function)
def get_call_stack_pdb(after_function="trace_dispatch",up_to_function="<module>"):
    """ Get the call stack in a 'pdb' debugger session, filtering out the 'pdb' functions that polute the graph. """
    return get_call_stack_after_up_to(after_function,up_to_function)

def stack_vscode(after_function="do_wait_suspend",up_to_function="<module>"):
    return get_call_stack_vscode(after_function, up_to_function)
def get_call_stack_vscode(after_function="do_wait_suspend",up_to_function="<module>"):
    """ Get the call stack in a 'vscode' debugger session, filtering out the 'vscode' functions that polute the graph. """
    return get_call_stack_after_up_to(after_function,up_to_function)

def stack_pycharm(after_function="trace_dispatch",up_to_function="<module>"):
    return get_call_stack_pycharm(after_function, up_to_function)
def get_call_stack_pycharm(after_function="trace_dispatch",up_to_function="<module>"):
    """ Get the call stack in a 'pycharm' debugger session, filtering out the 'pycharm' functions that polute the graph. """
    return get_call_stack_after_up_to(after_function,up_to_function)

def save_call_stack(filename):
    """ Saves the call stack to 'filename' for inspection to see what functions need to be 
    filtered out to create the desired graph. """
    with open(filename,'w') as file:
        for frame in inspect.stack():
            file.write(f"function:{frame.function} filename:{frame.filename}\n")

def print_call_stack_vars(stack_index=0):
    """ Prints all variables on the call stack. """
    for level, frameInfo in enumerate(reversed(inspect.stack())):
        print('=====',level,frameInfo.function)
        print(tuple(frameInfo.frame.f_locals.keys()))


# ------------ jupyter filtering

jupyter_filter_keys = {'exit','quit','v','In','Out','jupyter_filter_keys'}
def jupyter_locals_filter(jupyter_locals):
    """ Filter out the jupyter specific keys that polute the graph. """
    return {k:v for k,v in utils.filter_dict(jupyter_locals)
            if k not in jupyter_filter_keys and k[0] != '_'}

def locals_jupyter(stack_index=0):
    """ Get the locals of the calling frame in a jupyter notebook, filtering out the jupyter specific keys. """
    return jupyter_locals_filter(get_locals_from_call_stack(1+stack_index))

def stack_jupyter(up_to_function="<module>",stack_index=0):
    return get_call_stack_jupyter(up_to_function, 1+stack_index)
def get_call_stack_jupyter(up_to_function="<module>",stack_index=0):
    """ Get the call stack in a jupyter notebook, filtering out the jupyter specific keys. """
    call_stack = get_call_stack(up_to_function,1+stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = jupyter_locals_filter(call_stack[globals_frame])
    return call_stack


# ------------ ipython filtering

ipython_filter_keys = {'mg_visualization_status', 'sys', 'ipython', 'In', 'Out', 'get_ipython', 'exit', 'quit', 'open'}
def ipython_locals_filter(ipython_locals):
    """ Filter out the ipython specific keys that polute the graph. """
    return {k:v for k,v in utils.filter_dict(ipython_locals)
            if k not in ipython_filter_keys and k[0] != '_'}

def locals_ipython(stack_index=0):
    """ Get the locals of the calling frame in a ipython, filtering out the ipython specific keys. """
    return ipython_locals_filter(get_locals_from_call_stack(1+stack_index))

def stack_ipython(up_to_function="<module>",stack_index=0):
    return get_call_stack_ipython(up_to_function, 1+stack_index)
def get_call_stack_ipython(up_to_function="<module>",stack_index=0):
    """ Get the call stack in a ipython, filtering out the ipython specific keys. """
    call_stack = get_call_stack(up_to_function,1+stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = ipython_locals_filter(call_stack[globals_frame])
    return call_stack
