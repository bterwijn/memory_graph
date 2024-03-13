import Children
from Slicer import Slicer

def new(children):
    return Children_Linear(children) if children else None

class Children_Linear(Children.Children):
    slicer = Slicer(["1:-1:"])

    def __init__(self, children):
        sliced_children = Children_Linear.slicer.slice(children) if children else []
        super().__init__(sliced_children)

    def transform(self, fun):
        Children.transform(self.children, fun)

    def visit(self, fun):
        Children.visit(self.children, fun)
        