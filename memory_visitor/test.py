
def test_singular(fun):
    data = 100
    fun(data)

def test_linear(fun):
    data = [ 1, 2, 3, 4]
    fun(data)  

def test_key_value(fun):
    data = { 1:10, 2:20 }
    fun(data)

def test_class(fun):
    class My_Class:
        def __init__(self):
            self.a=10
            self.b=20
        def __repr__(self):
            return f'My_Class a:{self.a} b:{self.b}'
    data = [My_Class(), My_Class()]
    fun(data)

def test_all(fun):
    test_singular(fun)
    test_linear(fun)
    test_key_value(fun)
    test_class(fun)