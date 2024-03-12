import itertools
import collections
import time

def sliceable_front_back_split(sliceable, max_length):
    front_length, back_length = max_length
    total_length = front_length + back_length
    if total_length >= len(sliceable):
        return [sliceable[:total_length], []]
    front = min(len(sliceable), front_length)
    back = max(len(sliceable)-back_length, front)
    return [sliceable[:front], sliceable[back:]]

def sliceable_front_back_repeat_split(sliceable, size, line_size):
    index=0
    while (index < len(sliceable)):
        yield sliceable_front_back_split(sliceable[index:index+line_size],size)
        index += line_size

def empty_list(depth):
    empty = []
    for _ in range(depth-1):
        empty = [empty]
    return empty

def iterable_front_back_split(iterable, max_length, empty_list_depth):
    front_length, back_length = max_length
    total_length = front_length + back_length
    iterator = iter(iterable)
    if front_length > 0:
        total = list(itertools.islice(iterator, total_length))
        peek = list(itertools.islice(iterator, 1))
        if len(peek) == 0:
            return [total]
        if back_length == 0:
            return [total, empty_list(empty_list_depth)]
        front = total[:front_length]
        deque = collections.deque(total[front_length:]+peek, maxlen=back_length)
    else:
        front = empty_list(empty_list_depth)
        deque = collections.deque([], maxlen=back_length)
    deque.extend(iterable)
    back = list(deque)
    return [front, back]

def iterable_front_back_repeat_split_gen(iterable, size, line_size):
    iterator = iter(iterable)
    while (True):
        sliceable = list(itertools.islice(iterator, line_size))
        if len(sliceable) == 0:
            break
        yield front_back_split(sliceable, size)
def iterable_front_back_repeat_split(iterable, size, line_size):
    return list(iterable_front_back_repeat_split_gen(iterable, size, line_size))

def front_back_split(iterable, max_length, empty_list_depth=1):
    return iterable_front_back_split(iterable, max_length, empty_list_depth)

def front_back_repeat_split(iterable, max_length, line_size):
    return iterable_front_back_repeat_split(iterable, max_length, line_size)

class Child_Iterator: # not safe for nested lists, as list may contain lists of the structure and lists of data
    def __init__(self, stack_height, nested_list):
        self.stack_height = stack_height
        self.stack = [iter(nested_list)]
        self.level = 0
        self.empty_list = False

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            try:
                current_iterator = self.stack[-1]
                value = next(current_iterator)
                if len(self.stack) < self.stack_height:
                    if isinstance(value, list) and len(value) == 0:
                        self.empty_list = True
                    self.stack.append(iter(value))
                else:
                    diff_level = len(self.stack) - self.level
                    self.level = len(self.stack)
                    return (diff_level, value)
            except StopIteration:
                if self.empty_list:
                    self.empty_list = False
                    diff_level = len(self.stack) - self.level
                    self.level = len(self.stack)
                    return (-diff_level, None)
                self.stack.pop()
                self.level = len(self.stack)
        raise StopIteration

class Child_Iterator_Linear(Child_Iterator):

    def __init__(self, children):
        super().__init__(2, children)

class Child_Iterator_Key_Value(Child_Iterator):

    def __init__(self, children):
        super().__init__(2, children)

class Child_Iterator_Table(Child_Iterator):

    def __init__(self, children):
        super().__init__(4, children)

# general map does not work for nested lists, as list may contain lists of the structure and lists of data
# def map(data, fun):
#     child_iterator = Child_Iterator(data)
#     result = []
#     stack = [ result ]
#     stack_level = 0
#     append = True
#     for level,child in child_iterator:
#         #print('level,child:',level,child)
#         if level<0:
#             level = -level
#             append = False
#         else:
#             append = True
#         if level>0:
#             stack_level = max(stack_level-level,0)
#             for _ in range(level):
#                 new_list = []
#                 stack[stack_level].append(new_list)
#                 stack_level += 1
#                 if stack_level == len(stack):
#                     stack.append(new_list)
#                 else:
#                     stack[stack_level] = new_list
#         if append:
#             stack[stack_level].append( fun(child) )
#     return result[0]

class Children():
    def __init__(self, children=None):
        self.children = children

    def __repr__(self):
        return f'Children:{self.children}'

    def __len__(self):
        return len(self.children)

    def get_children(self):
        return self.children

    def __iter__(self):
        return Child_Iterator(self.children)


def map_linear(data, fun):
    return [ [fun(c) for c in front_back] for front_back in data]


class Children_Linear(Children):

    def __init__(self, children=None):
        super().__init__(children)

    def set_children(self, children, max_length):
        self.children = front_back_split(children, max_length)

    def __repr__(self):
        return f'Children_Linear:{self.children}'

    def map(self, fun):
        return Children_Linear(map_linear(self.children, fun))


def map_key_value(data, fun):
    return [ [fun(c) for c in front_back] for front_back in data]

class Children_Key_Value(Children):

    def __init__(self, children=None):
        super().__init__(children)

    def set_children(self, children, max_length):
        self.children = front_back_split(children, max_length)

    def __repr__(self):
        return f'Children_Key_Value:{self.children}'

    def map(self, fun):
        return Children_Key_Value(map_key_value(self.children, fun))

def map_table(data, fun):
    return [ [ [ [fun(c) for c in front_back] for front_back in row] for row in height] for height in data]

class Children_Table(Children):

    def __init__(self, children=None):
        super().__init__(children)

    def set_children(self, children, max_width, max_height, line_size=None):
        if line_size is None:
            self.children = [front_back_split(line, max_width) for line in children]
        else:
            self.children = front_back_repeat_split(children, max_width, line_size)
        self.children = front_back_split(self.children, max_height, 3)

    def __repr__(self):
        return f'Children_Table:{self.children}'

    def map(self, fun):
        return Children_Table(map_table(self.children,fun))

test_length=(3,2) # also test_width
test_height=(2,1)

def test_front_back_split(n):
    print("====== test_front_back_split")
    assert iterable_front_back_split([i for i in range(6)], (3,0)) == [[0,1,2], []]
    assert iterable_front_back_split([i for i in range(3)], (3,0)) == [[0,1,2]]
    assert iterable_front_back_split([i for i in range(6)], (3,2)) == [[0,1,2], [4,5]]
    assert iterable_front_back_split([i for i in range(5)], (3,2)) == [[0,1,2,3,4]]
    assert iterable_front_back_split([i for i in range(4)], (3,2)) == [[0,1,2,3]]
    assert iterable_front_back_split([i for i in range(6)], (0,3)) == [[], [3,4,5]]
    assert iterable_front_back_split([i for i in range(6)], (0,0)) == [[], []]

def test_front_back_repeat_split(n):
    print("====== test_front_back_repeat_split")
    assert iterable_front_back_repeat_split([i for i in range(6)], (3,2), 3) == [[[0,1,2]], [[3,4,5]]]
    assert iterable_front_back_repeat_split([i for i in range(20)], (3,2), 10) == [[[0,1,2],[8,9]], [[10,11,12],[18,19]]]
    assert iterable_front_back_repeat_split([i for i in range(22)], (3,2), 10) == [[[0,1,2],[8,9]], [[10,11,12],[18,19]], [[20,21]]]
    assert iterable_front_back_repeat_split([i for i in range(26)], (3,2), 10) == [[[0,1,2],[8,9]], [[10,11,12],[18,19]], [[20,21,22],[24,25]]]
    assert iterable_front_back_repeat_split([i for i in range(20)], (0,2), 10) == [[[],[8,9]], [[],[18,19]]]
    assert iterable_front_back_repeat_split([i for i in range(20)], (3,0), 10) == [[[0,1,2],[]], [[10,11,12],[]]]
    assert iterable_front_back_repeat_split([i for i in range(20)], (0,0), 10) == [[[],[]], [[],[]]]
    assert iterable_front_back_repeat_split([i for i in range(20)], (3,7), 10) == [[ list(range(0,10)) ],[ list(range(10,20)) ]]
    
    


def test_linear(n):
    print("\n\n\n====== test_linear")
    children = [i for i in range(n)]
    print("children:", children)
    children_linear = Children_Linear()
    children_linear.set_children(children, test_length)
    print( children_linear.map(lambda x: x*10) )

def test_key_value(n):
    print("====== test_key_value")
    children = list({i:i*2 for i in range(n)}.items())
    print("children:", children)
    children_key_value = Children_Key_Value()
    children_key_value.set_children(children, test_length)
    print( children_key_value.map(lambda kv: (kv[0]*10, kv[1]*100)) )

def test_table_1d(n):
    print("====== test_table_1d")
    children = [i for i in range(n*n)]
    print("children:", children)
    children_table = Children_Table()
    children_table.set_children(children, test_length, test_height, n)
    print(children_table)
    children_table = children_table.map(lambda x: x*10)
    print(children_table)

def test_table_2d(n):
    print("====== test_table_2d")
    children = [ [i*n+j for j in range(n)] for i in range(n)]
    print("children:", children)
    children_table = Children_Table()
    children_table.set_children(children, test_length, test_height)
    print(children_table)
    children_table = children_table.map(lambda x: x*10)
    print(children_table)
    for i in Child_Iterator_Table(children_table.get_children()):
        print(i)

def test_child_iterator():
    print("====== test_child_iterator")
    children = [[ [],  [1,2,3], [], [3,4,5] , [], []], [ [10,20], [] , [30,40]] ]
    print("children:", children)
    child_iterator = Child_Iterator(3, children)
    for level,child in child_iterator:
        print('level,child:',level,child)

# def speed_test_key_value(n,k, split_fun):
#     start_time = time.perf_counter()
#     children = {i:i*2 for i in range(n)}.items()
#     total_len = 0
#     children_key_value = Children_Key_Value()
#     for _ in range(k):
#         children_key_value.set_children(children, test_length, split_fun)
#         mapped = children_key_value.map(lambda kv: (kv[0]*10, kv[1]*100))
#         total_len+=len(mapped)
#     print(total_len)
#     elapsed_time = time.perf_counter() - start_time
#     print(f"Function executed in {elapsed_time} seconds.")

if __name__ == '__main__':
    n = 6
    test_front_back_split(n)
    test_front_back_repeat_split(n)

    test_linear(n)
    test_key_value(n)
    test_table_1d(n)
    test_table_2d(n)
    test_child_iterator()

    #test_iterator(n)
    # for fun in [lambda data,size : sliceable_front_back_split(list(data),size),
    #             iterable_front_back_split]: # sliceable slightly faster
    #     speed_test_key_value(20, 500000, fun)
    # TODO: sleep test
