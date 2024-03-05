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
        return node_layout.make_singular_body(self)

class Category_Linear(Category):

    def __init__(self, data, childeren):
        super().__init__(data, childeren)

    def get_body(self):
        return node_layout.make_linear_body(self)

class Category_Key_Value(Category):

    def __init__(self, data, childeren):
        super().__init__(data, childeren)
        
    def get_body(self):
        return node_layout.make_key_value_body(self)