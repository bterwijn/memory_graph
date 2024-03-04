import utils
import memory_visitor
import node_layout

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

class Category_Singular(Category):

    def __init__(self, data):
        super().__init__(data)

    def get_body(self):
        return node_layout.outer_table( 
                str(self.get_data()) 
                )

class Category_Linear(Category):

    def __init__(self, data, childeren):
        super().__init__(data, childeren)

    def get_body(self):
        s = '    '
        for i,c in enumerate(self.get_children()):
            s += f'<TD PORT="f{i}"> </TD>'
        return node_layout.outer_table(
                node_layout.inner_table( 
                    s
                ))

class Category_Key_Value(Category):

    def __init__(self, data, childeren):
        super().__init__(data, childeren)
        