
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

    
def get_type_name(data):
    return type(data).__name__
    
def nested_list(sizes, i=0, value=[0]):
    if i == len(sizes)-1:
        data = []
        for _ in range(sizes[i]):
            data.append( value[0] )
            value[0]+=1
    else:
        data = []
        for size in range(sizes[i]):
            data.append( nested_list(sizes,i+1) )
    return data

if __name__ == '__main__':
    print( nested_list([4,3,2]) )
