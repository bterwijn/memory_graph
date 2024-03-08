
class class_type:
    pass

def ignore_exception(func):
    try:
        return func()
    except Exception as e:
        pass

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

def avoid_html_injection(label):
    label=label.translate(str.maketrans({"<" : r"&lt;",
                                         ">" : r"&gt;",
                                         "&" : r"&amp;",
                                         "\"": r"&quot;",
                                         "\'": r"&apos;",
                                         }))
    return label

def to_string(data):
    return avoid_html_injection(str(data))


if __name__ == '__main__':
    ignore_exception(lambda x: 1/0)

