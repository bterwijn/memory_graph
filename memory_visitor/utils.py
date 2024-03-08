import types
import itertools
import collections

class class_type:
    pass

def ignore_exception(func):
    try:
        return func()
    except Exception as e:
        pass

def does_work(func):
    try:
        func()
        return True
    except Exception as e:
        return False

def has_dict_attribute(value):
    return hasattr(value,"__dict__")

def get_dict_attribute(value):
    return getattr(value,"__dict__")

def get_filtered_dict_attribute(value):
    return [(k,v) for k, v in get_dict_attribute(value).items() 
            if not k.startswith('__')]

def is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False
    
def is_self_iterating(data):
    return len(data)==1 and data == next(iter(data))

def get_type_name(data):
    return type(data).__name__

def front_back_split(iterable, size):
    front_size, back_size = size
    if isinstance(iterable, types.GeneratorType):
        return (tuple(itertools.islice(iterable, front_size)), 
                tuple(collections.deque(iterable, maxlen=back_size)))
    else:
        front = min(len(iterable), front_size)
        back = max(len(iterable)-back_size, front)
        return ((iterable[:front], iterable[back:]),)

def front_back_repeat_split(iterable, size, block_size):
    front_size, back_size = size
    if isinstance(iterable, types.GeneratorType):
        while True:
            block = tuple(itertools.islice(iterable, block_size))
            if not block:
                break
            yield front_back_split(block, size)
    else:
        index=0
        while (index < len(iterable)):
            next_index = min(index + block_size, len(iterable))
            front = min(len(iterable), index+front_size)
            back = max(next_index - back_size, front)
            yield (iterable[index:front], iterable[back:next_index])
            index = next_index

def transform_children(blocks, fun):
    block_out = []
    for block in blocks:
        front = [ fun(c) for c in block[0] ]
        back = [ fun(c) for c in block[1] ]
        block_out.append((front, back))
    return block_out
    
def print_return(data):
    print(data)
    return data

if __name__ == '__main__':
    ignore_exception(lambda x: 1/0)

    n = 13
    print( front_back_split([i for i in range(n)], (10, 5)) )
    print( front_back_split((i for i in range(n)), (10, 5)) )

    n = 16
    print( tuple(front_back_repeat_split([i for i in range(n)], (4, 3), 10)) )
    print( tuple(front_back_repeat_split((i for i in range(n)), (4, 3), 10)) )

    print( transform_children(front_back_repeat_split([i for i in range(n)], (4, 3), 10), lambda x: print_return(x)) )