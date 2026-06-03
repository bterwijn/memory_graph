# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import math 
import types
import functools
import traceback
import re
import html

import memory_graph.config as config

def limit_string(s):
    """ Limit the length of a string s to the 'max_string_length' in the config. """
    if len(s) > config.max_string_length:
        return s[:config.max_string_length] + '...'
    return s

def html_escape(s):
    """ Escape HTML characters in 's' for safe display in the graph. """
    return html.escape(s)

def newlines_to_br(s):
    """ Replace newlines in 's' with <BR/> tags for HTML display. """
    return s.replace('\n', ' <BR/> ')

def prep_str(s):
    """ Prepare 's' by limiting length, escaping HTML, and replacing newlines. """
    return newlines_to_br(html_escape(limit_string(s)))

def quote_string(s):
    """ Quote 's' if it is a string. """
    return "'" + s + "'"

def exception_to_string(e):
    """ Helper function to convert the traceback of an exception to a string. """
    return ''.join(traceback.format_exception(type(e), e, e.__traceback__)).strip()

def exception_to_string_no_path(e):
    """ Helper function to convert the traceback of an exception to a string without file paths. """
    s = exception_to_string(e)
    # Convert traceback file paths like File "/a/b/c.py" to File "c.py".
    def _strip_path(match):
        file_path = match.group(2).replace('\\', '/')  # for Windows paths
        file_name = file_path.rsplit('/', 1)[-1]
        return f'{match.group(1)}{file_name}{match.group(3)}'

    return re.sub(
        r'(^\s*File ")(.*?)(")',
        _strip_path,
        s,
        flags=re.MULTILINE,
    )

def exception_to_string_short(e):
    """ Helper function to convert an exception to a short string. """
    return f'{type(e).__name__}: {e}'

def mono_font(s):
    """ Helper function to wrap in monospaced font. """
    return f'<FONT FACE="Courier">{s}</FONT>'

def caret_line_length(s):
    """ Adds whitespace to caret line in 's' so it is as long as the previois line. """
    lines = s.split('\n')
    for i in range(len(lines)-2, -1, -1):
        if re.fullmatch(r'\s*~*\^+\s*', lines[i]):  # match line like '  ~~~^^ '
            lines[i] = lines[i].ljust(len(lines[i - 1]))
            break
    return '\n'.join(lines)

def prep_exception_str(s):
    """ Helper function to prepare an exception string for HTML display. """
    return newlines_to_br(mono_font(html_escape(caret_line_length(s))))

def get_all_types(obj):
    cls = type(obj)
    if hasattr(cls, '__mro__'):
        return cls.__mro__
    else:
        return [cls]

def has_dict_attributes(value):
    """ Returns 'True' if 'value' has a '__dict__' attribute. """
    return hasattr(value,"__dict__")

def get_dict_attributes(value):
    """ Returns the items of the '__dict__' attribute of 'value'."""
    return getattr(value,"__dict__")

def is_not_state(obj):
    """ Returns 'True' if 'obj' is not considered state, e.g. a function or method. """
    if isinstance(obj, (types.FunctionType, types.MethodType,
                        types.BuiltinFunctionType, types.BuiltinMethodType,
                        classmethod, staticmethod,
                        property, functools.partialmethod)):
        return True
    return type(obj).__name__ in {
        'method_descriptor',
        'builtin_function_or_method',
        'getset_descriptor',
        'classmethod_descriptor',
        'wrapper_descriptor',
        'member_descriptor',
        'method-wrapper',
    }

def filter_dict(dictionary):
    """ Filters out the unwanted dict attributes. """
    if '__name__' in dictionary: 
        return [ # filter classes and modules, no non-state allowed as values
            (k,v) for k, v in dictionary.items() if
            not (type(k) is str and k.startswith('__')) and
            not isinstance(v,types.ModuleType) and
            not is_not_state(v)
                ]
    return  [ # filter dictionaries, non-state allowed as values
            (k,v) for k, v in dictionary.items() if
            not (type(k) is str and k.startswith('__'))
            ]

def filter_type_attributes(tuples):
    """ Filters out the unwanted type attributes (class/static methods). """
    return [ # filter type objects, no non-state allowed as values
        (k,v) for k, v in tuples if
        not (type(k) is str and k.startswith('__')) and
        not is_not_state(v)
        ]

def make_sliceable(data):
    """ Returns a sliceble version of data, convert to list if not yet sliceble. """
    try:
        data[0:0]
        return data
    except TypeError:
        return list(data)
    except Exception:
        return []

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
