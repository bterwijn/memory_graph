import utils
import node_layout
import children

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
    
    def add_child(self, child): # TODO, remove this method
        self.children.append(child)

    def add_children(self, children):
        self.children = children

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
        super().__init__(data, None, alternative_type=alternative_type)

    def add_to_graph(self, graph):
        return node_layout.add_to_graph_singular(self,graph)

class Category_Linear(Category):
    max_length = (3,2)

    def __init__(self, data, candidate_children, alternative_type=None):
        children_linear = children.Children_Linear()
        children_linear.set_children(candidate_children, Category_Linear.max_length)
        super().__init__(data, children_linear, alternative_type)

    def add_to_graph(self, graph):
        return node_layout.add_to_graph_linear(self,graph)

class Category_Key_Value(Category):
    max_length = (3,2)

    def __init__(self, data, candidate_children, alternative_type=None):
        children_key_value = children.Children_Key_Value()
        children_key_value.set_children(candidate_children, Category_Key_Value.max_length)
        super().__init__(data, children_key_value, alternative_type)
        
    def add_to_graph(self, graph):
        return node_layout.add_to_graph_key_value(self,graph)

class Category_Table(Category):
    max_width = (0,0)
    max_height = (3,0)

    def __init__(self, data, candidate_children, alternative_type=None, size=None, row_names=None, column_names=None):
        children_table = children.Children_Table()
        children_table.set_children(candidate_children, 
                                    Category_Table.max_width, 
                                    Category_Table.max_height, 
                                    size[0])
        
        super().__init__(data, children_table, alternative_type)
        if size is None and row_names is not None and column_names is not None:
            size=(len(row_names),len(column_names))
        self.size=size
        self.row_names=row_names
        self.column_names=column_names

    def get_size(self):
        return self.size
    
    def get_row_names(self):
        return self.row_names
    
    def get_column_names(self):
        return self.column_names
        
    def add_to_graph(self, graph):
        return node_layout.add_to_graph_table(self,graph)