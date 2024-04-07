import types

# the types of the values we rewrite
ignore_types={types.FunctionType, types.MethodType, types.ModuleType}
try:
    ignore_types.add(types.GenericAlias) # only in python3.9 onwards
except AttributeError as e:
    pass
singular_types={type(None), bool, int, float, complex, str, range, bytes}
linear_types={tuple, list, set, frozenset, bytearray}
dict_types={dict,types.MappingProxyType}
dict_ignore_dunder_keys=True
custom_accessor_functions={}

def is_custom_accessor_type(value):
    return type(value) in custom_accessor_functions.keys()

def is_ignore_type(value):
    return type(value) in ignore_types

def is_singular_type(value):
    return type(value) in singular_types

def is_linear_type(value):
    return type(value) in linear_types

def is_dict_type(value):
    return type(value) in dict_types

def is_type_with_dict(value):
    return has_dict_attribute(value)

def is_generator_type(value):
    return type(value) is types.GeneratorType

def is_any_iterable(value):
    try:
        iter(value)
        return True
    except TypeError:
        return False

# functions that we rewrite the values with
    
def construct_singular(data,category): # default implementation just returns data
    return data

def construct_iterable(data,category): # default implementation makes a list
    return []
    
def add_to_iterable(iterable,data): # default implementation appends to list
    return iterable.append(data)

construct_singular_fun=construct_singular
construct_iterable_fun=construct_iterable
add_to_iterable_fun=add_to_iterable

# just some helper functions

def is_dunder_name(name):
    return name.startswith('__')

def has_dict_attribute(value):
    return hasattr(value,"__dict__")

def get_dict_attribute(value):
    return getattr(value,"__dict__")

# functions that traverse all the data recursively and call the rewrite functions

memo={} # remember all values to traverse each value only once

def rewrite_singular(singular,category):
    identifier=id(singular)
    if not identifier in memo:
        new_singular=construct_singular_fun(singular,category)
        memo[identifier]=new_singular
        return new_singular
    return memo[identifier]

def remember_or_construct_iterable(iterable,category):
    identifier=id(iterable)
    if not identifier in memo:
        memo[identifier]=construct_iterable_fun(iterable,category)
        return memo[identifier],True
    return memo[identifier],False

def rewrite_using_custom_accessor(data,category):
    new_iterable,is_just_constructed=remember_or_construct_iterable(data,category)
    if is_just_constructed:
        custom_result=custom_accessor_functions[type(data)](data)
        add_to_iterable_fun(new_iterable,rewrite(custom_result))
    return new_iterable

def rewrite_iterable(iterable,category):
    new_iterable,is_just_constructed=remember_or_construct_iterable(iterable,category)
    if is_just_constructed:
        for i in iterable:
            if not is_ignore_type(i):
                add_to_iterable_fun(new_iterable,rewrite(i))
    return new_iterable

def filter_dict(dictionary):
    for key in dictionary:
        if not type(key) is str or not is_dunder_name(key):
            if not is_ignore_type(key):
                value=dictionary[key]
                if not is_ignore_type(value):
                    yield (key,value)

def rewrite_dict(dictionary,category):
    new_iterable,is_just_constructed=remember_or_construct_iterable(dictionary,category)
    if is_just_constructed:
        for key,value in filter_dict(dictionary):
            add_to_iterable_fun(new_iterable,rewrite(key))
            add_to_iterable_fun(new_iterable,rewrite(value))
    return new_iterable

def rewrite_object_with_dict(obj,category):
    new_iterable,is_just_constructed=remember_or_construct_iterable(obj,category)
    if is_just_constructed:
        add_to_iterable_fun(new_iterable,rewrite(get_dict_attribute(obj)))
    return new_iterable

def rewrite(data):
    if is_custom_accessor_type(data):
        return rewrite_using_custom_accessor(data,"category_custom")
    elif is_ignore_type(data):
        return rewrite_singular("ignore_type","category_ignore")
    elif data is None:
        return rewrite_singular("None","category_singular") # special case, make a string because value 'None' is later used for not-specified in this software
    elif is_singular_type(data):
        return rewrite_singular(data,"category_singular")
    elif is_linear_type(data):
        return rewrite_iterable(data,"category_linear")
    elif is_dict_type(data):
        return rewrite_dict(data,"category_dict")
    elif is_type_with_dict(data):
        return rewrite_object_with_dict(data,"category_class")
    elif is_generator_type(data):
        return rewrite_singular(str(type(data)),"category_generator")
    elif is_any_iterable(data):
        return rewrite_iterable(data,"category_iterable")
    return rewrite_singular(str(data),"category_unkown") # unknown type

def rewrite_data(data):
    memo.clear() # forget all previous values
    return rewrite(data)
