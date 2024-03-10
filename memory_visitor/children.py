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

def iterable_front_back_split(iterable, size):
    front_size, back_size = size
    total_size = front_size + back_size
    iterator = iter(iterable)
    total = list(itertools.islice(iterator, total_size+1))
    if len(total) <= total_size:
        return [total, []]
    front = total[:front_size]
    deque = collections.deque(total[front_size:], maxlen=back_size)
    deque.extend(iterable)
    return [front, list(deque)]

def iterable_front_back_repeat_split_gen(iterable, size, line_size):
    iterator = iter(iterable)
    while (True):
        sliceable = list(itertools.islice(iterator, line_size))
        if len(sliceable) == 0:
            break
        yield sliceable_front_back_split(sliceable, size)

def iterable_front_back_repeat_split(iterable, size, line_size):
    return list(iterable_front_back_repeat_split_gen(iterable, size, line_size))

def front_back_split(iterable, size):
    return iterable_front_back_split(iterable, size)

def front_back_repeat_split(iterable, size, line_size):
    return iterable_front_back_repeat_split(iterable, size, line_size)

class Child_Iterator:
    def __init__(self, nested_list):
        self.stack = [iter(nested_list)]
        self.level = 0
        self.empty = False

    def __iter__(self):
        return self

    def __next__(self):
        while self.stack:
            try:
                current_iterator = self.stack[-1]
                value = next(current_iterator)
                if isinstance(value, list):
                    if (len(value) == 0):
                        self.empty = True
                    self.stack.append(iter(value))
                else:
                    diff_level = len(self.stack) - self.level
                    self.level = len(self.stack)
                    return (diff_level, value)
            except StopIteration:
                if self.empty: # special case for iterating over empty list
                    self.empty = False
                    diff_level = len(self.stack) - self.level
                    self.level = len(self.stack)
                    return (-diff_level, None)
                self.stack.pop()
                self.level = len(self.stack)
        raise StopIteration

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

    
class Children_Linear(Children):
    
    def __init__(self, children=None):
        super().__init__(children)

    def set_children(self, children, size):
        self.children = front_back_split(children, size)

    def __repr__(self):
        return f'Children_Linear:{self.children}'
    
    def map(self, fun):
        return Children_Linear([ [fun(c) for c in front_back] for front_back in self.children])

class Children_Key_Value(Children):

    def __init__(self, children=None):
        super().__init__(children)
    
    def set_children(self, children, size):
        self.children = front_back_split(children, size)

    def __repr__(self):
        return f'Children_Key_Value:{self.children}'
    
    def map(self, fun):
        return Children_Key_Value([ [fun(c) for c in front_back] for front_back in self.children])

class Children_Table(Children):

    def __init__(self, children=None):
        super().__init__(children)

    def set_children(self, children, size, line_size=None):
        if line_size is None:
            self.children = [front_back_split(line, size) for line in children]
        else:
            self.children = front_back_repeat_split(children, size, line_size)
            print("self.children:", self.children)

    def __repr__(self):
        return f'Children_Table:{self.children}'
    
    def map(self, fun):
        return Children_Table([[ [fun(c) for c in front_back] for front_back in row] for row in self.children])

test_size=(3,2)

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
    print("\n\n\n====== test_linear")
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

def test_child_iterator():
    print("====== test_child_iterator")
    data = [[ [], [1,2], [], [3,4], []]]
    print(data)
    for i in Child_Iterator(data):
        print(i)
    print('mapped:',map(data, lambda x: x) )

def test_iterator(n):
    print("====== test_iterator")
    children = [ [i*n+j for j in range(n)] for i in range(n)]
    print("children:", children)
    children_table = Children_Table()
    children_table.set_children(children, test_size)
    print("children_table:", children_table)
    for i in children_table:
        print(i)
    print( children_table.map(lambda x: x) )

# def speed_test_key_value(n,k, split_fun):
#     start_time = time.perf_counter()
#     children = {i:i*2 for i in range(n)}.items()
#     total_len = 0
#     children_key_value = Children_Key_Value()
#     for _ in range(k):
#         children_key_value.set_children(children, test_size, split_fun)
#         mapped = children_key_value.map(lambda kv: (kv[0]*10, kv[1]*100))
#         total_len+=len(mapped)
#     print(total_len)
#     elapsed_time = time.perf_counter() - start_time
#     print(f"Function executed in {elapsed_time} seconds.")

if __name__ == '__main__':
    n = 5
    test_iterable_front_back_split(n)
    test_iterable_front_back_repeat_split(n)

    test_linear(n)
    test_key_value(n)
    test_table_1d(n)
    test_table_2d(n)

    test_child_iterator()
    test_iterator(n)
    # for fun in [lambda data,size : sliceable_front_back_split(list(data),size), 
    #             iterable_front_back_split]: # sliceable slightly faster
    #     speed_test_key_value(20, 500000, fun)
    # TODO: sleep test
    