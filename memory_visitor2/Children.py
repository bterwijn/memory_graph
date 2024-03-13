

def transform(children, fun):
    print('children1:', children)
    for block in children:
        for i in range(len(block)):
            if block[i]:
                block[i] = fun(block[i])
    print('children2:', children)

def visit(children, fun):
    for block in children:
        for c in block:
            if c:
                fun(c)

class Children:
    
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return f'Children({self.children})'
    