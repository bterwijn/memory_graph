from memory_graph import rewrite

def my_construct_singular(data,category):
    return str(data)

def my_construct_iterable(data,category):
    return []
    
def my_add_to_iterable(iterable,data):
    return iterable.append(data)

rewrite.construct_singular_fun=my_construct_singular
rewrite.construct_iterable_fun=my_construct_iterable
rewrite.add_to_iterable_fun=my_add_to_iterable

def show(data):
    print( rewrite.rewrite_data(data) )

def test():
    l=[4,5]
    data=[ l,l,(100,200)]
    print(data)
    show( data )
    
if __name__ == "__main__":
    test()
