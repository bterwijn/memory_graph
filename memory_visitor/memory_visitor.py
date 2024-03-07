import types
import utils
import categories
import test

no_reference_types = {bool, int, float, complex, str} # bytes, bytearray, type(None)}

type_to_category = {
    str: lambda data: categories.Category_Singular(data), # visit as whole string
    dict: lambda data: categories.Category_Key_Value(data, data.items())
    }

ignore_types={types.FunctionType, types.MethodType, types.ModuleType, types.GeneratorType}
utils.ignore_exception( lambda: ignore_types.add(types.CoroutineType) )



def default_backtrack_callback(categorized):
    print('default_backtrack categorized:',categorized)

visit_backtrack_callback = default_backtrack_callback

def categorize(data):
    if type(data) in type_to_category: # for predefined types
        return type_to_category[type(data)](data)
    elif utils.has_dict_attribute(data): # for user defined classes
        return categories.Category_Key_Value(data, utils.get_dict_attribute(data).items(), utils.class_type)
    elif utils.is_iterable(data): # for lists, tuples, sets, ...
        return categories.Category_Linear(data,data)
    return categories.Category_Singular(data) # for int, float, str, ...

def visit_recursive(data, parent_categorized):
    if (parent_categorized != None and type(data) in no_reference_types):
        return str(data)
    if type(data) in ignore_types:
        return None
    if categories.Category.is_already_categorized(data):
        categorized = categories.Category.get_categorized(data)
    else:
        categorized = categorize(data)
        categorized.set_parent(parent_categorized)
        for c in categorized.get_candidate_children():
            categorized_child = visit_recursive(c, categorized)
            if categorized_child:
                categorized.add_child(categorized_child)
        visit_backtrack_callback(categorized)
    return categorized

def visit(data):
    categories.Category.clear_visited_ids()
    visit_recursive(data,None)

if __name__ == '__main__':
    test.test_all( visit )
