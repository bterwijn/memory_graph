import memory_graph as mg

class Base:

    def __init__(self, n):
        self.elements = [1]
        iter = self.elements
        for i in range(2,n):
            iter.append([i])
            iter = iter[-1]

    def get_last(self):
        iter = self.elements
        while len(iter)>1:
            iter = iter[-1]
        return iter
            
class A(Base):

    def __init__(self, n):
        super().__init__(n)

class B(Base):

    def __init__(self, n):
        super().__init__(n)

class C(Base):

    def __init__(self, n):
        super().__init__(n)

a = A(6)
b1 = B(6)
b2 = B(6)
c = C(6)

x = ['x']
b2.get_last().append(x)

mg.config.type_to_depth[B] = 3
mg.config.type_to_depth[id(c)] = 2
mg.render(locals(), 'introspect_depth.png')
