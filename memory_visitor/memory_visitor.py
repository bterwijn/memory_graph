import types
import utils
import categories

visited_ids = {}
ignore_types={types.FunctionType, types.MethodType, types.ModuleType, types.GeneratorType}
utils.ignore_exception( lambda: ignore_types.add(types.CoroutineType) )

get_children_for_types = {
    dict: lambda d: tuple(d.items())
    }

def has_dict_attribute(value):
    return hasattr(value,"__dict__")

def get_dict_attribute(value):
    return [getattr(value,"__dict__")]

def is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False

def default_visit_callback(category,parent_category):
    print('default_visit category:',category)
    print('                parent:',parent_category)
    pass

def default_backtrack_callback(category):
    print('default_backtrack category:',category)
    pass

visit_callback = default_visit_callback
visit_backtrack_callback = default_backtrack_callback

def categorize(data):
    if is_iterable(data):
        return categories.Category_Linear(data,data)
    return categories.Category_Singular(data)

def visit_recursive(data, parent_category):
    if id(data) in visited_ids or type(data) in ignore_types:
        return
    visited_ids[id(data)] = len(visited_ids)
    category = categorize(data)
    visit_callback(category, parent_category)
    for c in category.get_children():
        visit_recursive(c, category)
    visit_backtrack_callback(category)

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
