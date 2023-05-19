from memory_graph import rewrite
from memory_graph import Node
from memory_graph import rewrite_to_node
from memory_graph import grapviz_nodes

__version__ = "0.1.0"
__author__ = 'Bas Terwijn'

def show(data,block=True):
    graph=create(data)
    graph.view()
    if block:
        input(f"showing '{graph.filename}', press <ENTER> to continue...")

def render(data,output_filename=None,block=True):
    graph=create(data)
    if output_filename:
        graph.render(outfile=output_filename)
        if block:
            input(f"rendering '{output_filename}', press <ENTER> to continue...")
    else:
        graph.render()
        if block:
            input(f"rendering '{graph.filename}', press <ENTER> to continue...")

def create(data):
    all_nodes=rewrite_to_node.rewrite_data(data)
    return grapviz_nodes.create_graph(all_nodes)

def test():
    blocking=True

    #rewrite_to_node.reduce_references=False # don't reduce references
    
    class TestClass:
        s1=1000
        s2=[1,2,3]
        def __init__(self):
            self.a=99
            self.b=(1,2)
    data=[TestClass(),TestClass()]
    show(data,block=blocking)
    render(data,"graph.png",block=False)
    
    # test data
    s1="hello world"
    l1=[1,2,3,s1]

    data=[l1]
    #show(data,block=blocking)
    #render(data,"test.pdf")
    
    t1=(10,20,30,40)
    #data.append(t1)
    #show(data,block=blocking)
    d1={'k1':t1, 'k2':1234, 'k3':s1}
    #data.append(d1)
    #show(data,block=blocking)
    class MyClass:
        static1=1000
        static2=t1
        def __init__(self):
            self.a=l1
            self.b=t1
            self.c=s1
            self.d=d1
        def set_ref(self,r):
            self.ref=r
    c1=MyClass()
    show(c1,block=blocking)
    
    data.append(c1)
    show(data,block=blocking)
    data.append(10000088)
    show(data,block=blocking)
    
    l1.append(data) # recursive
    d1["k4"]=data
    c1.set_ref(data)
    #print(data)
    show(data,block=blocking)

    for i in range(10):
        data.append(i)
        show(data,block=blocking)

    show(locals(),block=blocking) # locals
    #show(Node.all_nodes,block) # all_nodes

