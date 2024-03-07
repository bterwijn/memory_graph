import utils
import memory_visitor
import node_layout

class Category:
    visited_ids = {}

    def clear_visited_ids():
        Category.visited_ids.clear()

    def is_already_categorized(data):
        return id(data) in Category.visited_ids
    
    def get_categorized(data):
        return Category.visited_ids[id(data)]

    def __init__(self, data, candidate_children, alternative_type):
        self.data = data
        self.parent = None
        self.candidate_children = candidate_children
        self.alternative_type = alternative_type
        self.children = []
        self.is_subgraphed_flag = False
        self.name = f'node{len(Category.visited_ids)}'
        Category.visited_ids[id(data)] = self

    def __repr__(self):
        return f'{type(self).__name__} data:{self.data} type:{self.get_type_name()} children:{self.children}'

    def get_data(self):
        return self.data
    
    def set_parent(self, parent):
        self.parent = parent

    def get_parent(self):
        return self.parent
    
    def get_alternative_type(self):
        return self.alternative_type
    
    def get_candidate_children(self):
        return self.candidate_children
    
    def add_child(self, child):
        self.children.append(child)

    def get_children(self):
        return self.children
    
    def get_type_name(self):
        return utils.get_type_name(self.data)
    
    def get_node_name(self):
        return self.name
    
    def set_subgraphed(self):
        self.is_subgraphed_flag = True
        return self

    def is_subgraphed(self):
        return self.is_subgraphed_flag
    
    def get_node_and_edges(self):
        pass

class Category_Singular(Category):

    def __init__(self, data, alternative_type=None ):
        super().__init__(data, tuple(), alternative_type=alternative_type)

    def get_node_and_edges(self):
        return node_layout.get_node_and_edges_singular(self)

class Category_Linear(Category):

    def __init__(self, data, children, alternative_type=None):
        super().__init__(data, children, alternative_type)

    def get_node_and_edges(self):
        return node_layout.get_node_and_edges_linear(self)

class Category_Key_Value(Category):

    def __init__(self, data, children, alternative_type=None):
        super().__init__(data, children, alternative_type)
        
    def get_node_and_edges(self):
        return node_layout.get_node_and_edges_key_value(self)