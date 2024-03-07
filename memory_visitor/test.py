
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
    data = { 1:10, 2:20 }
    fun(data)

def test_class(fun):
    class My_Class:
        def __init__(self):
            self.foo=10
            self.bar=20
        def __repr__(self):
            return f'My_Class foo:{self.foo} bar:{self.bar}'
    data = [My_Class(), My_Class()]
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

def test_all(fun):
    test_singular(fun)
    test_string(fun)
    test_linear(fun)
    test_empty_linear(fun)
    test_key_value(fun)
    test_class(fun)
    test_share_tuple(fun)
    test_share_children(fun)