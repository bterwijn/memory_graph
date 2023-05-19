from types import NoneType
from types import MappingProxyType

def has_dict_attribute(value):
    return hasattr(value,"__dict__")

def get_dict_attribute(value):
    return getattr(value,"__dict__")

def has_class_attribute(value):
    return hasattr(value,"__class__")

def get_class_attribute(value):
    return getattr(value,"__class__")

def get_name_attribute(value):
    return getattr(value,"__name__")

# the types of the values we rewrite

singular_types={NoneType, bool, int, float, complex, str, type}
linear_types={tuple, list, set, frozenset, bytearray}
dict_types={dict, MappingProxyType}
known_types=singular_types | linear_types | dict_types

def is_singular_type(value):
    return type(value) in singular_types

def is_linear_type(value):
    return type(value) in linear_types

def is_dict_type(value):
    return type(value) in dict_types

def is_known_type(value):
    return type(value) in known_types

def is_class_type(value):
    return not is_known_type(value) and has_dict_attribute(value)

def is_iterable_type(value):
    return is_linear_type(value) or is_dict_type(value) or is_class_type(value)

def type_name(value):
    return get_name_attribute(type(value))

def is_dunder_name(name):
    return name.startswith('__') and name.endswith('__')

# functions that we rewrite the values with
    
def construct_singular(data): # default implementation just returns data
    return data

def construct_iterable(data): # default implementation makes a list
    return []
    
def add_to_iterable(iterable,data): # default implementation appends to list
    return iterable.append(data)

construct_singular_fun=construct_singular
construct_iterable_fun=construct_iterable
add_to_iterable_fun=add_to_iterable

# functions that traverse all the data recursively and call the rewrite functions

memo={} # remember all values to traverse each value only once

def rewrite_singular(singular):
    identifier=id(singular)
    if not identifier in memo:
        new_singular=construct_singular_fun(singular)
        memo[identifier]=new_singular
        return new_singular
    return memo[identifier]

def remember_or_construct_iterable(iterable,identifier=None):
    if identifier is None:
        identifier=id(iterable)
    if not identifier in memo:
        memo[identifier]=construct_iterable_fun(iterable)
        return memo[identifier],True
    return memo[identifier],False

def rewrite_iterable(iterable):
    new_iterable,is_constructed=remember_or_construct_iterable(iterable)
    if is_constructed:
        for i in iterable:
            add_to_iterable_fun(new_iterable,rewrite(i))
    return new_iterable

def rewrite_dict(dictionary):
    new_iterable,is_constructed=remember_or_construct_iterable(dictionary)
    if is_constructed:
        for key in dictionary:
            add_to_iterable_fun(new_iterable,rewrite(key))
            add_to_iterable_fun(new_iterable,rewrite(dictionary[key]))
    return new_iterable

def rewrite_class_dictionary(class_type): # special case for class_dictionary of class_type
    class_dictionary=get_dict_attribute(class_type) # class_dictionary is of type MappingProxyType, and its id() keeps changing
    class_type_id=id(class_type)
    if class_type_id in memo:
        return memo[class_type_id]
    keys=[key for key in class_dictionary if (not type(key) is str or not is_dunder_name(key)) and is_known_type(class_dictionary[key])]
    if len(keys)>0: # only if it has items we want to rewrite
        new_iterable,is_constructed=remember_or_construct_iterable(class_dictionary,class_type_id) # therefore use id() of class_type instead
        if is_constructed:
            for key in keys:
                add_to_iterable_fun(new_iterable,rewrite(key))
                add_to_iterable_fun(new_iterable,rewrite(class_dictionary[key]))
        return new_iterable
    return None
                
def rewrite_object(obj):
    new_iterable,is_constructed=remember_or_construct_iterable(obj)
    if is_constructed:
        new_class_dictionary = rewrite_class_dictionary(get_class_attribute(obj))
        if new_class_dictionary:
            add_to_iterable_fun(new_iterable,new_class_dictionary)
        add_to_iterable_fun(new_iterable,rewrite(get_dict_attribute(obj)))
    return new_iterable

def rewrite(data):
    if type(data) is NoneType:
        return rewrite_singular("None") # special case, make a string because value 'None' is used for not-specified in software
    elif is_singular_type(data):
        return rewrite_singular(data)
    elif is_linear_type(data):
        return rewrite_iterable(data)
    elif is_dict_type(data):
        return rewrite_dict(data)
    elif is_class_type(data):
        return rewrite_object(data)
    return rewrite_singular("??"+type_name(data)+"??") # unknown type

def rewrite_data(data):
    memo.clear() # forget all previous values
    return rewrite(data)

