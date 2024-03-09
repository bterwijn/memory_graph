import itertools
import collections
import time

def sliceable_front_back_split(sliceable, size):
    front_size, back_size = size
    total_size = front_size + back_size
    if total_size >= len(sliceable):
        return [sliceable[:total_size], []]
    front = min(len(sliceable), front_size)
    back = max(len(sliceable)-back_size, front)
    return [sliceable[:front], sliceable[back:]]

def sliceable_front_back_repeat_split(sliceable, size, line_size):
    front_size, back_size = size
    index=0
    while (index < len(sliceable)):
        yield sliceable_front_back_split(sliceable[index:index+line_size],size)
        index += line_size
        # next_index = min(index + line_size, len(sliceable))
        # front = min(len(sliceable), index+front_size)
        # back = max(next_index - back_size, front)
        # yield (sliceable[index:front], sliceable[back:next_index])
        # index = next_index

# def iterable_front_back_split(iterable, size):
#     front_size, back_size = size
#     iterator = iter(iterable)
#     return list(itertools.islice(iterator, front_size)), collections.deque(iterator, maxlen=back_size)

# def iterable_front_back_repeat_split(iterable, size, line_size):
#     while (True):
#         sliceable = list(itertools.islice(iterable, line_size))
#         if len(sliceable) == 0:
#             break
#         yield sliceable_front_back_split(sliceable, size)

class Children():
    def __init__(self, children=None):
        self.children = children

    def __repr__(self):
        return f'Children:{self.children}'

    def __len__(self):
        return len(self.children)

    def get_children(self):
        return self.children

class Children_Linear(Children):
    
    def __init__(self, children=None):
        super().__init__(children)

    def set_children(self, children, size, split_fun=sliceable_front_back_split):
        self.children = split_fun(children, size)

    def __repr__(self):
        return f'Children_Linear:{self.children}'
    
    def map(self, fun):
        return Children_Linear([ [fun(c) for c in front_back] for front_back in self.children])

class Children_Key_Value(Children):

    def __init__(self, children=None):
        super().__init__(children)
    
    def set_children(self, children, size, split_fun=sliceable_front_back_split):
        self.children = split_fun(children, size)

    def __repr__(self):
        return f'Children_Key_Value:{self.children}'
    
    def map(self, fun):
        return Children_Key_Value([ [fun(c) for c in front_back] for front_back in self.children])

class Children_Table(Children):

    def __init__(self, children=None):
        super().__init__(children)

    def set_children(self, children, size, line_size=None,
                    split_fun_1d=sliceable_front_back_split,
                    split_fun_2d=sliceable_front_back_repeat_split):
        if line_size is None:
            self.children = [split_fun_1d(line, size) for line in children]
        else:
            self.children = split_fun_2d(children, size, line_size)

    def __repr__(self):
        return f'Children_Table:{self.children}'
    
    def map(self, fun):
        return Children_Table([[ [fun(c) for c in front_back] for front_back in row] for row in self.children])

test_size=(3,2)

# def test_iterable_front_back_split(n):
#     print("====== test_iterable_front_back_split")
#     children = [i for i in range(n)]
#     print("children:", children)
#     front_back = iterable_front_back_split(iter(children), (3,2))
#     print("front_back:", list(front_back))

# def test_iterable_front_back_repeat_split(n):
#     print("====== test_iterable_front_back_repeat_split")
#     children = [i for i in range(n*n)]
#     print("children:", children)
#     front_back = iterable_front_back_repeat_split(iter(children), (3,2), n)
#     print("front_back:", list(front_back))

def test_linear(n):
    print("\n\n\n\n\n====== test_linear")
    children = [i for i in range(n)]
    print("children:", children)
    children_linear = Children_Linear()
    children_linear.set_children(children, test_size)
    print( children_linear.map(lambda x: x*10) )

def test_key_value(n):
    print("====== test_key_value")
    children = list({i:i*2 for i in range(n)}.items())
    print("children:", children)
    children_key_value = Children_Key_Value()
    children_key_value.set_children(children, test_size)
    print( children_key_value.map(lambda kv: (kv[0]*10, kv[1]*100)) )

def test_table_1d(n):
    print("====== test_table_1d")
    children = [i for i in range(n*n)]
    print("children:", children)
    children_table = Children_Table()
    children_table.set_children(children, test_size, n)
    print( children_table.map(lambda x: x*10) )

def test_table_2d(n):
    print("====== test_table_2d")
    children = [ [i*n+j for j in range(n)] for i in range(n)]
    print("children:", children)
    children_table = Children_Table()
    children_table.set_children(children, test_size)
    print( children_table.map(lambda x: x*10) )

def speed_test_key_value(n,k, split_fun):
    start_time = time.perf_counter()
    children = {i:i*2 for i in range(n)}.items()
    total_len = 0
    children_key_value = Children_Key_Value()
    for _ in range(k):
        children_key_value.set_children(children, test_size, split_fun)
        mapped = children_key_value.map(lambda kv: (kv[0]*10, kv[1]*100))
        total_len+=len(mapped)
    print(total_len)
    elapsed_time = time.perf_counter() - start_time
    print(f"Function executed in {elapsed_time} seconds.")

if __name__ == '__main__':
    n = 5
    # test_iterable_front_back_split(n)
    # test_iterable_front_back_repeat_split(n)

    test_linear(n)
    test_key_value(n)
    test_table_1d(n)
    test_table_2d(n)
    # for fun in [lambda data,size : sliceable_front_back_split(list(data),size), 
    #             iterable_front_back_split]: # sliceable slightly faster
    #     speed_test_key_value(20, 500000, fun)
    