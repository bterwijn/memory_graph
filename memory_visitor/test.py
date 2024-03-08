import memory_visitor
import categories
import node_layout

def test_singular(fun):
    data = 100
    fun(data)

def test_linear(fun):
    data = [None, True, 1, 2.2, complex(3,4), 'hello']
    fun(data)

def test_linears(fun):
    data = [(1,2), [3,4], {5,6}, frozenset((7,8)), {9:'9', 10:'10'} , bytes('11', 'utf-8'), bytearray('12', 'utf-8')]
    fun(data)

def test_empty_linear(fun):
    data = [tuple(), list(), set(), frozenset(), dict() , bytes(), bytearray()]
    fun(data)

def test_key_value(fun):
    data1 = {1:'a', 2:'b', 3:'c', 4:'d'}
    data2 = data1.copy()
    data2[3] = ('c','c')
    data = {'first':data1, 'second':data2}
    fun(data)

def test_class(fun):
    class My_Class1:
        def __init__(self):
            self.foo=10
            self.bar=20
    class My_Class2:
        def __init__(self):
            self.foo=10
            self.bar=20
    data = [My_Class1(), My_Class2()]
    node_layout.no_drop_child_references_types.add(My_Class1)  # TODO
    memory_visitor.no_reference_types.remove(str)
    fun(data)
    memory_visitor.no_reference_types.add(str)

def test_class_vars(fun):
    class My_Class1:
        class_var1 = 'a'
        class_var2 = 'b'
        def __init__(self):
            self.var1=10
            self.var2=20
    data = [My_Class1, My_Class1()]
    fun(data)

def test_share_tuple(fun):
    class My_Class:
        def __init__(self):
            self.a=1
    data = [('a',1), ('a',1), {'a':1}, {'a':1}, My_Class(),My_Class()]
    fun(data)

def test_share_children(fun):
    a=['a']
    b=['b']
    c=['c']
    d=['d']
    data = [ [a,b,c,], [a,c,d] ]
    fun(data)

def test_table(fun):
    class My_Table:
        def __init__(self,size):
            self.size=size
            self.data = [i for i in range(size[0]*size[1])]
    data = My_Table((3,4))
    data.data[1] = (1,)
    data.data[5] = (5,)
    data.data[6] = (6,)
    data.data[8] = (8,)
    memory_visitor.type_to_category[My_Table] = lambda data: (
        categories.Category_Table(  data,
                                    data.data,
                                    size = data.size,
                                    row_names = [f'row{i}' for i in range(data.size[0])],
                                    column_names = [f'col{i}' for i in range(data.size[1])])
    )
    fun(data)

def test_all(fun):
    test_singular(fun)
    test_linear(fun)
    test_linears(fun)
    test_empty_linear(fun)
    test_key_value(fun)
    test_class(fun)
    test_class_vars(fun)
    test_share_tuple(fun)
    test_share_children(fun)
    test_table(fun)