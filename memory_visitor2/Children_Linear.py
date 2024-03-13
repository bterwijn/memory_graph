import Children
from Slicer import Slicer

def new(children):
    return Children_Linear(children) if children else None

def fill_html_table_helper(html_table, depth, child):
    if depth == 1:
        html_table.add_dots()
    if child:
        html_table.add_column(f'{child.get_data()}')
    
class Children_Linear(Children.Children):
    slicer = Slicer(["1:-1:"])

    def __init__(self, children):
        sliced_children = Children_Linear.slicer.slice(children) if children else []
        super().__init__(sliced_children)

    def transform(self, fun):
        Children.transform(self.children, fun)

    def visit(self, fun):
        Children.visit(self.children, fun)
        
    def fill_html_table(self, node, html_table):
        Children.visit_with_depth(self.children, lambda depth_child : fill_html_table_helper(html_table,depth_child[0],depth_child[1]) )
    