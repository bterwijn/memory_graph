# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph.memory_to_nodes as memory_to_nodes
import memory_graph.config as config
import memory_graph.config_default
import memory_graph.utils as utils

import inspect
import sys
import itertools as it
from memory_graph.call_stack import call_stack

import graphviz
from typing import List, Tuple

# Add 'mg' to builtins so it is available in all subsequent imports
import memory_graph as mg
import builtins
if not hasattr(builtins, "mg"):
    builtins.mg = mg

__version__ = "0.3.50"
__author__ = 'Bas Terwijn'

last_show_filename = None
render_filename_count = 0

def get_source_location(stack_index=0):
    """ Helper function to get the source location of the stack with 'stack_index' of the call stack. """
    frameInfo = inspect.stack()[1+stack_index] # get frameInfo of calling frame
    filename= frameInfo.filename
    line_nr= frameInfo.lineno
    function = frameInfo.function
    return f'{filename}:{line_nr} in "{function}"'

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
    if memory_graph.config.block_prints_location:
        print('blocked at ' + get_source_location(1+stack_index), end=', ')
    if memory_graph.config.press_enter_message:
        print(memory_graph.config.press_enter_message)
    input()
    return result

def create_graph(data):
    """ Creates and returns a memory graph from 'data'. """
    return memory_to_nodes.memory_to_nodes(data)

def number_filename(outfile):
    """ Returns the 'outfile' with 'render_filename_count'. """
    global render_filename_count
    splits = outfile.split('.')
    if len(splits)>1:
        splits[-2]+=str(render_filename_count)
        render_filename_count += 1
        return '.'.join(splits)
    return outfile

def render(data, outfile=None, view=False, numbered = False):
    """ Renders the graph of 'data' to 'outfile' or `memory_graph.render_filename` when not specified. """
    if outfile is None:
        outfile = memory_graph.config.render_filename
    graph = create_graph(data)
    if numbered:
        outfile = number_filename(outfile)
    if outfile.endswith('.gv') or outfile.endswith('.dot'):
        graph.save(filename=outfile)
    else:
        graph.render(outfile=outfile, view=view, cleanup=False, quiet=False, quiet_view=False)


def show(data, outfile=None, view=False, numbered = False):
    """ Shows the graph of 'data' by first rendering and then opening the default viewer
    application by file extension at first call, when the outfile changes, or
    when view is True. """
    if outfile is None:
        outfile = memory_graph.config.render_filename
    open_view = (outfile != memory_graph.last_show_filename) or view or config.reopen_viewer
    render(data=data, outfile=outfile, view=open_view, numbered=numbered)
    memory_graph.last_show_filename = outfile


# ------------ aliases

def sl(stack_index=0):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.show(data)
    
def ss(stack_index=0):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.show(data)

def bsl(stack_index=0):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.show, data, stack_index=1+stack_index)
    
def bss(stack_index=0):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.show, data, stack_index=1+stack_index)

def rl(stack_index=0):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.render(data)
    
def rs(stack_index=0):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.render(data)

def brl(stack_index=0):
    """ 
    Shows the graph of locals() and blocks. 
    """
    data = get_locals_from_call_stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.render, data, stack_index=1+stack_index)
    
def brs(stack_index=0):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    data = stack(stack_index=1+stack_index)
    memory_graph.block(memory_graph.render, data, stack_index=1+stack_index)

def l(stack_index=0):
    """ 
    Shows the graph of locals() and blocks. 
    """
    bsl(stack_index=1+stack_index)
    
def s(stack_index=0):
    """ 
    Shows the graph of mg.stack() and blocks. 
    """
    bss(stack_index=1+stack_index)


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

def stack_begin_index(stack_functions : List[str], begin_functions : List[Tuple[str, int]]):
    """ Returns the index of stack_functions that matches the first name in
    'begin_functions' and adds corresponding 'offset'. """
    for func, offset in begin_functions:
        try:
            return stack_functions.index(func) + offset
        except ValueError:
            pass
    return 0

def stack_end_index(stack_functions : List[str], begin_index : int, end_functions : List[str]):
    """ Returns the index starting from 'begin_index' of stack_functions that
    matches the first name in end_functions. """
    for func in end_functions:
        try:
            return stack_functions.index(func, begin_index)
        except ValueError:
            pass
    return len(stack_functions)-1



def stack_slice(begin_functions : List[Tuple[str, int]] = [],
                end_functions : List[str] = ["<module>"],
                stack_index : int = 0,
                frameInfos : List[inspect.FrameInfo] = None):
    """
    Returns a slice of the call stack.
    Parameters:
      begin_functions - list of (function-name, offset), begins at the index of the first
                        'function-name' that is found in the call stack with additional 'offset',
                        otherwise begins at index 0
      end_functions - list of function-names, ends at the index of the first 'function-name'
                          that is found in the call stack after begin index (inclusive),
                          otherwise ends at the last index
      stack_index - number of frames removed from the beginning
    """
    if frameInfos == None:
        frameInfos = inspect.stack()
    stack_functions = [s.function for s in frameInfos]
    begin_index = stack_begin_index(stack_functions, begin_functions)
    end_index = stack_end_index(stack_functions, begin_index, end_functions)
    return stack_frames_to_dict(reversed(frameInfos[begin_index+stack_index:end_index+1]))

def stack(end_functions=["<module>"], stack_index=0):
    return stack_slice([], end_functions, stack_index+2)

def stack_pdb(begin_functions=[("trace_dispatch",1)],
              end_functions=["<module>"],
              stack_index=0):
    """ Get the call stack in a 'pdb' debugger session, filtering out the 'pdb' functions that polute the graph. """
    return stack_slice(begin_functions, end_functions, stack_index)

def stack_vscode(begin_functions=[("_line_event",1), ("_return_event",1), ("do_wait_suspend",1), ("_do_wait_suspend",2)],
                 end_functions=["<module>"],
                 stack_index=0):
    """ Get the call stack in a 'vscode' debugger session, filtering out the 'vscode' functions that polute the graph. """
    return stack_slice(begin_functions, end_functions, stack_index)

def stack_cursor(begin_functions=[("_line_event",1), ("_return_event",1), ("do_wait_suspend",1), ("_do_wait_suspend",2)],
                 end_functions=["<module>"],
                 stack_index=0):
    """ Get the call stack in a 'cursor' debugger session, filtering out the 'cursor' functions that polute the graph. """
    return stack_slice(begin_functions, end_functions, stack_index)

def stack_pycharm(begin_functions=[("py_line_callback",1), ("py_return_callback",1), ("do_wait_suspend",2)],
                  end_functions=["<module>"],
                  stack_index=0):
    """ Get the call stack in a 'pycharm' debugger session, filtering out the 'pycharm' functions that polute the graph. """
    return stack_slice(begin_functions, end_functions, stack_index)

def stack_wing(begin_functions=[("_py_line_event",1), ("_py_return_event",1)],
               end_functions=["<module>"],
               stack_index=0):
    """ Get the call stack in a 'wing' debugger session, filtering out the 'wing' functions that polute the graph. """
    return stack_slice(begin_functions, end_functions, stack_index)


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

# ------------ IDE aliases 

def vscode(filename=None, data=None):
    if data is None:
        data = stack_vscode()
    render(data, filename)

def cursor(filename=None, data=None):
    if data is None:
        data = stack_cursor()
    render(data, filename)

def pycharm(filename=None, data=None):
    if data is None:
        data = stack_pycharm()
    render(data, filename)

def wing(filename=None, data=None):
    if data is None:
        data = stack_wing()
    render(data, filename)


# ------------ jupyter filtering

jupyter_filter_keys = {'mg_visualization_status', 'exit','quit','v','In','Out','jupyter_filter_keys'}
def jupyter_locals_filter(jupyter_locals):
    """ Filter out the jupyter specific keys that polute the graph. """
    return {k:v for k,v in utils.filter_dict(jupyter_locals)
            if k not in jupyter_filter_keys and k[0] != '_'}

def locals_jupyter(stack_index=0):
    """ Get the locals of the calling frame in a jupyter notebook, filtering out the jupyter specific keys. """
    return jupyter_locals_filter(get_locals_from_call_stack(1+stack_index))

def stack_jupyter(end_functions=["<module>"],stack_index=0):
    """ Get the call stack in a jupyter notebook, filtering out the jupyter specific keys. """
    call_stack = stack(end_functions,1+stack_index)
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

def stack_ipython(end_functions=["<module>"], stack_index=0):
    """ Get the call stack in a ipython, filtering out the ipython specific keys. """
    call_stack = stack(end_functions,1+stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = ipython_locals_filter(call_stack[globals_frame])
    return call_stack

# ------------ google colab filtering

colab_filter_keys = {'In', 'Out', 'exit', 'quit'}
def colab_locals_filter(colab_locals):
    """ Filter out the colab specific keys that polute the graph. """
    return {k:v for k,v in utils.filter_dict(colab_locals)
            if k not in colab_filter_keys and k[0] != '_'}

def locals_colab(stack_index=0):
    """ Get the locals of the calling frame in a colab, filtering out the colab specific keys. """
    return colab_locals_filter(get_locals_from_call_stack(1+stack_index))

def stack_colab(end_functions=["<cell line: 0>", "<module>"], stack_index=0):
    """ Get the call stack in a colab, filtering out the colab specific keys. """
    call_stack = stack(end_functions,1+stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = colab_locals_filter(call_stack[globals_frame])
    return call_stack

# ------------ marimo filtering

marimo_filter_keys = {'spec_from_loader', '__marimo__', '__builtin__', '_MicropipLoader', '_MicropipFinder'}
def marimo_locals_filter(marimo_locals):
    """ Filter out the marimo specific keys that polute the graph. """
    return {k:v for k,v in utils.filter_dict(marimo_locals)
            if k not in marimo_filter_keys and k[0] != '_'}

def locals_marimo(stack_index=0):
    """ Get the locals of the calling frame in a marimo, filtering out the marimo specific keys. """
    return marimo_locals_filter(get_locals_from_call_stack(1+stack_index))

def stack_marimo(end_functions=["<cell line: 0>", "<module>"], stack_index=0):
    """ Get the call stack in a marimo, filtering out the marimo specific keys. """
    call_stack = stack(end_functions,1+stack_index)
    globals_frame = next(iter(call_stack))
    call_stack[globals_frame] = marimo_locals_filter(call_stack[globals_frame])
    return call_stack
