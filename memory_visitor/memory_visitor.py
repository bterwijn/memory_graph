import types
import utils
import categories
import node_layout

no_reference_types = {type(None), bool, int, float, complex, str}

type_to_category = {
    str: lambda data: categories.Category_Singular(data), # visit as whole string, don't iterate over characters
    dict: lambda data: categories.Category_Key_Value(data, list(data.items())),
    set: lambda data: categories.Category_Linear(data, list(data)), #TODO, iterate!
    }

ignore_types={types.FunctionType, types.MethodType, types.ModuleType, types.GeneratorType}
utils.ignore_exception( lambda: ignore_types.add(types.CoroutineType) ) # python 3.5 onwards


def default_backtrack_callback(categorized):
    print('default_backtrack categorized:',categorized)

visit_backtrack_callback = default_backtrack_callback

def categorize(data):
    if type(data) in type_to_category: # for predefined types
        return type_to_category[type(data)](data)
    elif utils.has_dict_attribute(data): # for user defined classes
        return categories.Category_Key_Value(data, 
                                            list(utils.get_filtered_dict_attribute(data)), 
                                            utils.class_type)
    elif utils.is_iterable(data): # for lists, tuples, sets, ...
        return categories.Category_Linear(data,data)
    return categories.Category_Singular(data) # for int, float, str, ...

def visit_recursive(data, parent_categorized):
    #print('visit_recursive: ',data, parent_categorized)
    if (parent_categorized != None and type(data) in no_reference_types):
        return node_layout.format_string(data)
    if type(data) in ignore_types:
        return None
    if categories.Category.is_already_categorized(data):
        categorized = categories.Category.get_categorized(data)
    else:
        categorized = categorize(data)
        categorized.set_parent(parent_categorized)
        candidate_children = categorized.get_candidate_children()
        if candidate_children:
            categorized_children = candidate_children.map( lambda child : visit_recursive(child, categorized) )
            categorized.add_children(categorized_children)
        visit_backtrack_callback(categorized)
    return categorized

def visit(data):
    categories.Category.clear_visited_ids()
    visit_recursive(data,None)

if __name__ == '__main__':
    import test
    test.test_all( visit )
