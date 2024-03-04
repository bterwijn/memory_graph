import utils
import memory_visitor

class Category:

    def __init__(self, data, children=tuple()):
        self.data = data
        self.children = children

    def __repr__(self):
        return f'{type(self).__name__} data:{self.data} type:{self.get_type_name()} childeren:{self.children}'

    def get_data(self):
        return self.data
    
    def get_children(self):
        return self.children
    
    def get_type_name(self):
        return utils.get_type_name(self.data)
    
    def get_node_name(self):
        return memory_visitor.get_node_name(self.data)
    
    def get_body(self):
        pass

def begin_table():
    return '<\n<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="blue"><TR><TD PORT="X">\n'
def end_table():
    return '</TD></TR></TABLE>>\n'

class Category_Singular(Category):

    def __init__(self, data):
        super().__init__(data)

    def get_body(self):
        body  = begin_table()
        body += str(self.get_data())
        body += end_table()
        return body

def begin_subtable():
    return '  <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="4" CELLPADDING="0"><TR>\n'
def end_subtable():
    return '\n  </TR></TABLE>\n'

class Category_Linear(Category):

    def __init__(self, data, childeren):
        super().__init__(data, childeren)

    def get_body(self):
        body  = begin_table()
        if len(self.get_children())>0:
            body += begin_subtable()
            for i,c in enumerate(self.get_children()):
                body += f'<TD PORT="f{i}"> </TD>'
            body += end_subtable()
        body += end_table()
        return body

class Category_Key_Value(Category):

    def __init__(self, data, childeren):
        super().__init__(data, childeren)
        