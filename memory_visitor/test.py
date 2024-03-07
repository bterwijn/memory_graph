import memory_visitor
import categories
import node_layout

def test_singular(fun):
    data = 100
    fun(data)

def test_string(fun):
    data = "hello world!"
    fun(data)

def test_linear(fun):
    data = [ 1, 2, 3]
    fun(data)  

def test_empty_linear(fun):
    data = [ [], [], []]
    fun(data)

def test_key_value(fun):
    data = { 1:'a', 2:'b' }
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
    data = [My_Class2()]
    node_layout.no_drop_child_references_types.add(My_Class1)
    memory_visitor.no_reference_types.remove(str)
    fun(data)
    memory_visitor.no_reference_types.add(str)

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
    memory_visitor.type_to_category[My_Table] = lambda data: categories.Category_Table(data, data.data, data.size)
    fun(data)

def test_all(fun):
    test_singular(fun)
    test_string(fun)
    test_linear(fun)
    test_empty_linear(fun)
    test_key_value(fun)
    test_class(fun)
    test_share_tuple(fun)
    test_share_children(fun)
    test_table(fun)