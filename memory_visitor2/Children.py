

def transform(children, fun):
    for block in children:
        for i in range(len(block)):
            block[i] = fun(block[i])

def visit(children, fun):
    for block in children:
        for c in block:
            fun(c)

class Children:
    
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return f'Children({self.children})'
    