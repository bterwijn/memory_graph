import types
import utils
import categories

visited_ids = {}
ignore_types={types.FunctionType, types.MethodType, types.ModuleType, types.GeneratorType}
utils.ignore_exception( lambda: ignore_types.add(types.CoroutineType) )

get_children_for_types = {
    dict: lambda data: categories.Category_Key_Value(data,tuple(data.items())) 
    }

def has_dict_attribute(value):
    return hasattr(value,"__dict__")

def get_dict_attribute(value):
    return tuple(getattr(value,"__dict__").items())

def is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False

def default_visit_callback(categorized,parent_categorized):
    print('default_visit categorized:',categorized)
    print('                parent:',parent_categorized)
    pass

def default_backtrack_callback(categorized):
    print('default_backtrack categorized:',categorized)
    pass

visit_callback = default_visit_callback
visit_backtrack_callback = default_backtrack_callback

def categorize(data):
    if type(data) in get_children_for_types:
        return get_children_for_types[type(data)](data)
    elif has_dict_attribute(data): # classes
        return categories.Category_Key_Value(data, get_dict_attribute(data))
    elif is_iterable(data):
        return categories.Category_Linear(data,data)
    return categories.Category_Singular(data)

def visit_recursive(data, parent_categorized):
    if id(data) in visited_ids or type(data) in ignore_types:
        return
    visited_ids[id(data)] = len(visited_ids)
    categorized = categorize(data)
    visit_callback(categorized, parent_categorized)
    for c in categorized.get_children():
        visit_recursive(c, categorized)
    visit_backtrack_callback(categorized)

def visit(data):
    visited_ids.clear()
    visit_recursive(data,None)

def get_node_name(data):
    return 'node'+str(visited_ids[id(data)])

# class My_Class:

#     def __init__(self):
#         self.a=10
#         self.b=20
#         self.c=30

if __name__ == '__main__':
    data = 100
    data = [ 1, 2 ]
    #data = { 1:10, 2:20 }
    #data = (My_Class(),My_Class())
    visit(data)
