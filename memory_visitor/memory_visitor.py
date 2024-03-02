import types

visited_ids = {}
ignore_types={types.FunctionType, types.MethodType, types.ModuleType}
try:
    ignore_types.add(types.GenericAlias) # only in python3.9 onwards
except AttributeError as e:
    pass

get_children_for_types = {
    list: lambda d: d
    }

def default_visit_callback(data,parent):
    #print('default_visit data:',data,'parent:',parent)
    pass

def default_backtrack_callback(data,children):
    #print('default_backtrack data:',data,'children:',children)
    pass

visit_callback = default_visit_callback
visit_backtrack_callback = default_backtrack_callback

def is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False

def get_children(data):
    children = ()
    if type(data) in get_children_for_types:
        children = get_children_for_types[type(data)](data)
    elif is_iterable(data): # iterate is default visitor for not specified types
        children = data
    if isinstance(children, types.GeneratorType):
        children=tuple(children)
    return children

def visit_recursive(data,parent):
    if id(data) in visited_ids or type(data) in ignore_types:
        return
    visited_ids[id(data)] = len(visited_ids)
    visit_callback(data,parent)
    children = get_children(data)
    for i in children:
        visit_recursive(i,data)
    visit_backtrack_callback(data,children)

def visit(data):
    visited_ids.clear()
    visit_recursive(data,None)

def get_id(data):
    return visited_ids[id(data)]

if __name__ == '__main__':
    data = [ [1], [2] ]
    visit(data)
