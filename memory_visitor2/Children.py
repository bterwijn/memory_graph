

def transform(children, fun):
    for block in children:
        for i in range(len(block)):
            block[i] = fun(block[i])

def visit(children, fun):
    for block in children:
        for c in block:
            fun(c)

# class Child_Iterator:
#     def __init__(self, stack_height, nested_list):
#         self.stack_height = stack_height
#         self.stack = [iter(nested_list)]
#         self.level = 0
#         self.empty_list = False

#     def __iter__(self):
#         return self

#     def __next__(self):
#         while self.stack:
#             try:
#                 current_iterator = self.stack[-1]
#                 value = next(current_iterator)
#                 if len(self.stack) < self.stack_height:
#                     if isinstance(value, list) and len(value) == 0:
#                         self.empty_list = True
#                     self.stack.append(iter(value))
#                 else:
#                     diff_level = len(self.stack) - self.level
#                     self.level = len(self.stack)
#                     return (diff_level, value)
#             except StopIteration:
#                 if self.empty_list:
#                     self.empty_list = False
#                     diff_level = len(self.stack) - self.level
#                     self.level = len(self.stack)
#                     return (-diff_level, None)
#                 self.stack.pop()
#                 self.level = len(self.stack)
#         raise StopIteration


def visit_with_depth(children, fun):
    depth = 2
    for block in children:
        if len(block) == 0:
            fun( (depth, None) )
        depth = 1
        for c in block:
            fun( (depth, c) )
            depth = 0
        depth = 1

def inner_html_table(s):
    return ('<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5" CELLPADDING="0"><TR>\n' +
            s + '\n</TR></TABLE>')

def add_html_column(s, c):
    s += f'<TD> {s} </TD>'

def add_html_new_line(s):
    s += '</TR>\n<TR>'

def add_dots(s):
    s += '<TD>...</TD>'

class Children:
    
    def __init__(self, children):
        self.children = children

    def __repr__(self):
        return f'Children({self.children})'
