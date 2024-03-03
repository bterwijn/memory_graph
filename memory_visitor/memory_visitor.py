import types

visited_ids = {}
ignore_types={types.FunctionType, types.MethodType, types.ModuleType, types.GeneratorType}
try:
    ignore_types.add(types.GenericAlias) # only in python3.9 onwards
except AttributeError as e:
    pass

get_children_for_types = {
    dict: lambda d: tuple(d.items())
    }

def has_dict_attribute(value):
    return hasattr(value,"__dict__")

def get_dict_attribute(value):
    return getattr(value,"__dict__")

def is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False
    

def default_visit_callback(data,parent):
    print('default_visit data:',data,' type:',type(data))
    print('            parent:',parent,' type:',type(parent))
    pass

def default_backtrack_callback(data,children):
    print('default_backtrack data:',data,' type:',type(data))
    print('              children:',children, ' types:',[type(c) for c in children])
    pass

visit_callback = default_visit_callback
visit_backtrack_callback = default_backtrack_callback



def get_children(data):
    children = ()
    if type(data) in get_children_for_types:
        children = get_children_for_types[type(data)](data)
    elif has_dict_attribute(data):
        children = [get_dict_attribute(data)]
    elif is_iterable(data):
        children = data
    return children

def visit_recursive(data,parent):
    if id(data) in visited_ids or type(data) in ignore_types:
        return
    visited_ids[id(data)] = len(visited_ids)
    visit_callback(data,parent)
    children = get_children(data)
    for c in children:
        visit_recursive(c,data)
    visit_backtrack_callback(data,children)

def visit(data):
    visited_ids.clear()
    visit_recursive(data,None)

def get_id(data):
    return visited_ids[id(data)]

class My_Class:

    def __init__(self):
        self.a=10
        self.b=20
        self.c=30

if __name__ == '__main__':
    data = [ [1], [2] ]
    data = { 1:10, 2:20 }
    data = My_Class()
    visit(data)
