
def ignore_exception(func):
    try:
        return func()
    except Exception as e:
        pass

def has_dict_attribute(value):
    return hasattr(value,"__dict__")

def get_dict_attribute(value):
    return getattr(value,"__dict__").items()

def is_iterable(data):
    try:
        iter(data)
        return True
    except TypeError:
        return False

def get_type_name(data):
    return type(data).__name__

if __name__ == '__main__':
    ignore_exception(lambda x: 1/0)

