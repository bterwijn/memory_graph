# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import math 
import types

def has_dict_attributes(value):
    """ Returns 'True' if 'value' has a '__dict__' attribute. """
    return hasattr(value,"__dict__")

def get_dict_attributes(value):
    """ Returns the items of the '__dict__' attribute of 'value'."""
    return getattr(value,"__dict__")

def is_function(obj):
    if isinstance(obj, types.FunctionType) or isinstance(obj, types.MethodType):
        return True
    return type(obj).__name__ in {'method_descriptor', 'builtin_function_or_method', 'getset_descriptor', 'classmethod_descriptor'}

def filter_dict(dictionary):
    """ Filters out the unwanted dict attributes. """
    if '__name__' in dictionary: # only filter stack frames, for example locals()
        return [
            (k,v) for k, v in dictionary.items() if
            not k == "memory_graph" and
            not (type(k) is str and k.startswith('__')) and
            not isinstance(v,types.ModuleType) and
            not is_function(v)
                ]
    return dictionary.items()

def filter_type_attributes(tuples):
    """ Filters out the unwanted type attributes (class/static methods). """
    return [
        (k,v) for k, v in tuples if
        not (type(k) is str and k.startswith('__')) and
        not type(v) in {classmethod, staticmethod} and
        not callable(v)
            ]

def make_sliceable(data):
    """ Returns a sliceble version of data, convert to list if not yet sliceble. """
    try:
        data[0:0]
        return data
    except TypeError:
        return list(data)

def is_finite_iterable(data):
    """ Returns 'True' if 'data' is finite iterable. """
    try:
        iter(data) # iterable
        len(data)  # and not infinite (not a strong test, but what else?)
        return True
    except TypeError:
        return False
    
def get_type_name(data):
    """ Returns the name of the type of 'data'. """
    return type(data).__name__
    
def nested_list(sizes, i=0, value=[0]):
    """ Returns a nested list with the given 'sizes' for test purposes. """
    if i == len(sizes)-1:
        data = []
        for _ in range(sizes[i]):
            data.append( value[0] )
            value[0]+=1
    else:
        data = []
        for size in range(sizes[i]):
            data.append( nested_list(sizes,i+1) )
    return data

def my_round(value):
    """ Rounds the value to the nearest integer rounding '.5' up consistantly. """
    return math.floor(value + 0.5)

def generator_has_data(generator):
    """ Returns 'True' if the generator has data. """
    try:
        next(generator)
        return True
    except StopIteration:
        return False

def take_up_to(condition, iterable):
    for i in iterable:
        yield i
        if condition(i):
            return

def take_after(condition, iterable):
    taking = False
    for i in iterable:
        if taking:
            yield i
        elif condition(i):
            taking = True

if __name__ == '__main__':
    print( nested_list([4,3,2]) )
