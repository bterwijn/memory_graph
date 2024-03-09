import itertools
import collections

def sliceable_front_back_split(sliceable, size):
    front_size, back_size = size
    front = min(len(sliceable), front_size)
    back = max(len(sliceable)-back_size, front)
    return [sliceable[:front], sliceable[back:]]

def sliceable_front_back_repeat_split(sliceable, size, line_size):
    front_size, back_size = size
    index=0
    while (index < len(sliceable)):
        next_index = min(index + line_size, len(sliceable))
        front = min(len(sliceable), index+front_size)
        back = max(next_index - back_size, front)
        yield (sliceable[index:front], sliceable[back:next_index])
        index = next_index

def iterable_front_back_split(iterable, size):
    front_size, back_size = size
    yield (list(itertools.islice(iterable,front_size)), collections.deque(iterable, maxlen=back_size))

def iterable_front_back_repeat_split(iterable, size, line_size):
    while (True):
        sliceable = list(itertools.islice(iterable, line_size))
        if len(sliceable) == 0:
            break
        yield sliceable_front_back_split(sliceable, size)

class Children:

    def __init__(self):
        pass

    def get_size(self):
        return (3,2)

class Children_Linear(Children):
    
    def __init__(self, children):
        super().__init__()
        self.children = iterable_front_back_split(children, self.get_size())

    def __repr__(self):
        return f'children:{self.children}'
    
    def map(self, fun):
        return [ [fun(c) for c in front_back] for front_back in self.children]

class Children_Key_Value(Children):
    
    def __init__(self, children):
        super().__init__()
        self.children = sliceable_front_back_split(list(children), self.get_size()) #TODO: list?

    def __repr__(self):
        return f'children:{self.children}'
    
    def map(self, fun):
        return [ [(fun(k),fun(v)) for k,v in front_back] for front_back in self.children]

class Children_Table(Children):
    
    def __init__(self, children, line_size=None):
        super().__init__()
        if line_size is None:
            self.children = [iterable_front_back_split(line, self.get_size()) for line in children]
        else:
            self.children = sliceable_front_back_repeat_split(children, self.get_size(), line_size)

    def __repr__(self):
        return f'children:{self.children}'
    
    def map(self, fun):
        return [[ [fun(c) for c in front_back] for front_back in row] for row in self.children]

def test_iterable_front_back_split(n):
    print("====== test_iterable_front_back_split")
    children = [i for i in range(n)]
    print("children:", children)
    front_back = iterable_front_back_split(iter(children), (3,2))
    print("front_back:", list(front_back))

def test_iterable_front_back_repeat_split(n):
    print("====== test_iterable_front_back_repeat_split")
    children = [i for i in range(n*n)]
    print("children:", children)
    front_back = iterable_front_back_repeat_split(iter(children), (3,2), n)
    print("front_back:", list(front_back))

def test_linear(n):
    print("====== test_linear")
    children = [i for i in range(n)]
    print("children:", children)
    children_linear = Children_Linear(children)
    print(children_linear)
    print( children_linear.map(lambda x: x) )

def test_key_value(n):
    print("====== test_key_value")
    children = {i:i*2 for i in range(n)}.items()
    print("children:", children)
    children_key_value = Children_Key_Value(children)
    print(children_key_value)
    print( children_key_value.map(lambda x: x) )

def test_table_1d(n):
    print("====== test_table_1d")
    children = [i for i in range(n*n)]
    print("children:", children)
    children_table = Children_Table(children, n)
    print(children_table)
    print( list(children_table.map(lambda x: x)) )

def test_table_2d(n):
    print("====== test_table_2d")
    children = [ [i*n+j for j in range(n)] for i in range(n)]
    print("children:", children)
    children_table = Children_Table(children)
    print(children_table)
    print( list(children_table.map(lambda x: x)) )

if __name__ == '__main__':
    n = 7
    test_iterable_front_back_split(n)
    test_iterable_front_back_repeat_split(n)
    test_linear(n)
    test_key_value(n)
    test_table_1d(n)
    test_table_2d(n)
