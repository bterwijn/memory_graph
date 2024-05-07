import memory_graph.utils as utils
import memory_graph.config as config
import memory_graph.config_helpers as config_helpers
from memory_graph.sequence import Sequence1D

class Element_Base:
    """
    Element_Base represents a node in the memory graph. This base class has different subclasses for different types of nodes.
    """
    
    """
    Create a Element_Base object.
    """
    def __init__(self, data, children=None):
        self.data = data
        self.children = Sequence1D([]) if children is None else children
        self.parent_indices = {}

    def __repr__(self):
        """
        Return a string representation of the node showing the original data represented by the node.
        """
        #return f'data: {self.data} children: {self.children} parents: {self.parents}'
        return f'{self.get_type_name()} id:{self.get_id()} parent_indices:{self.parent_indices}'

    def add_parent_index(self, parent, parent_index):
        """
        Add a parent to the node.
        """
        if not parent in self.parent_indices:
            self.parent_indices[parent] = []
        self.parent_indices[parent].append(parent_index)

    def get_parent_indices(self):
        return self.parent_indices

    def get_id(self):
        """
        Return the id of the node.
        """
        return id(self.data)

    def __eq__(self, other):
        """
        Return if the node is equal to another node.
        """
        return self.get_id() == other.get_id()
    
    def __hash__(self):
        """
        Return the hash of the node.
        """
        return self.get_id()

    def get_data(self):
        """
        Return the original data represented by the node.
        """
        return self.data
    
    def get_type(self):
        """
        Return the type of the data represented by the node.
        """
        return type(self.data)
    
    def get_type_name(self):
        """
        Return the name of the type of the data represented by the node.
        """
        return utils.get_type_name(self.data)

    # def has_children(self):
    #     """
    #     Return the number of children of the node.
    #     """
    #     return not self.children is None

    def get_children(self):
        """
        Return the children of the node. Initially the children are raw data, but 
        later they too are converted to Element_Base by the Memory_visitor using the Element_Base 'transform' method.
        """
        return self.children

    def get_name(self):
        """
        Return a unique name for the node.
        """
        return f'node{self.get_id()}'
    
    def get_html_table(self, slices, graph_sliced):
        """
        Return the HTML_Table object that determines how the node is visualized in the graph.
        """
        from memory_graph.html_table import HTML_Table
        html_table = HTML_Table()
        if self.children is None:
            html_table.add_string(f'{self.data}')
        else:
            self.fill_html_table(html_table, slices, graph_sliced)
        return html_table
    
    def get_slicer(self):
        return config_helpers.get_slicer(self, self.get_data())

    def is_node(self):
        """
        Return if the node is a separate node in the graph.
        """
        return not self.get_type() in config.no_reference_types
    
    def is_hidden_node(self):
        """
        Return if the node is a hidden node in the graph.
        """
        from memory_graph.element_key_value import Element_Key_Value
        return self.get_type() is tuple and len(self.children) == 1 and type(self.children[0]) is Element_Key_Value

    # -------------------- Element_Base interface, overriden by subclasses --------------------

    def fill_html_table(self, html_table, slices, graph_sliced):
        """
        Fill the HTML_Table object with each child of the node.
        """
        pass

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        return self.get_type_name()