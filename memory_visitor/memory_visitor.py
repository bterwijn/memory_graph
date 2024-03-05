import types
import utils
import categories
import test

type_to_category = {
    dict: lambda data: categories.Category_Key_Value(data, data.items())
    }

ignore_types={types.FunctionType, types.MethodType, types.ModuleType, types.GeneratorType}
utils.ignore_exception( lambda: ignore_types.add(types.CoroutineType) )

visited_ids = {}

def default_visit_callback(categorized,parent_categorized):
    print('default_visit categorized:',categorized)
    print('                   parent:',parent_categorized)

def default_backtrack_callback(categorized):
    print('default_backtrack categorized:',categorized)

visit_callback = default_visit_callback
visit_backtrack_callback = default_backtrack_callback

def categorize(data):
    if type(data) in type_to_category: # for predefined types
        return type_to_category[type(data)](data)
    elif utils.has_dict_attribute(data): # for classes
        return categories.Category_Key_Value(data, utils.get_dict_attribute(data))
    elif utils.is_iterable(data): # for lists, tuples, sets, ...
        return categories.Category_Linear(data,data)
    return categories.Category_Singular(data) # for int, float, str, ...

def visit_recursive(data, parent_categorized):
    if type(data) in ignore_types:
        return False
    if id(data) not in visited_ids:
        visited_ids[id(data)] = len(visited_ids)
        categorized = categorize(data)
        visit_callback(categorized, parent_categorized)
        for c in categorized.get_candidate_children():
            if visit_recursive(c, categorized):
                categorized.add_child(c)
        visit_backtrack_callback(categorized)
    return True

def visit(data):
    visited_ids.clear()
    visit_recursive(data,None)

def get_node_name(data):
    return 'node'+str(visited_ids[id(data)])

if __name__ == '__main__':
    test.test_all( visit )
