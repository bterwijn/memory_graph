import math 
import types

def has_dict_attributes(value):
    return hasattr(value,"__dict__")

def get_dict_attributes(value):
    return getattr(value,"__dict__").items()

def filter_dict_attributes(tuples):
    #print('tuples:', tuples)
    return [(k,v) for k, v in tuples 
            if type(k) is str and not k.startswith('__') 
            and not isinstance(v,types.ModuleType)
            and not isinstance(v,types.FunctionType)]

def is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False
    
def has_no_children(children):
    return len(children) == 1 and len(children[0]) == 0
    
def get_type_name(data):
    return type(data).__name__
    
def nested_list(sizes, i=0, value=[0]):
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
    return math.floor(value + 0.5)

def generator_has_data(generator):
    try:
        next(generator)
        return True
    except StopIteration:
        return False

if __name__ == '__main__':
    print( nested_list([4,3,2]) )
