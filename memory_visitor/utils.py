
def ignore_exception(func):
    try:
        return func()
    except Exception as e:
        pass

def get_type_name(data):
    return type(data).__name__


if __name__ == '__main__':
    ignore_exceptions(lambda x: 1/0)

