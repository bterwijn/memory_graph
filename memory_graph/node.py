import memory_graph.utils as utils
import memory_graph.config as config
import memory_graph.config_helpers as config_helpers

class Node:
    """
    Node represents a node in the memory graph. This base class has different subclasses for different types of nodes.
    """
    
    """
    Create a Node object.

    Args:
        data (object): The data represented by the node.
        children (list): The children of the node.
        size (string): The size of the node to be shown in the graph.
    """
    def __init__(self, data, children=None):
        self.data = data
        self.children = children

    def __repr__(self):
        """
        Return a string representation of the node showing the original data represented by the node.
        """
        return f'{utils.get_type_name(self)} children:{self.children}'

    def get_id(self):
        """
        Return the id of the node.
        """
        return id(self.data)

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

    def has_children(self):
        """
        Return the number of children of the node.
        """
        return not self.children is None

    def get_children(self):
        """
        Return the children of the node. Initially the children are raw data, but 
        later they too are converted to Node by the Memory_visitor using the Node 'transform' method.
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


    # -------------------- Node interface, overriden by subclasses --------------------

    def fill_html_table(self, html_table, slices, graph_sliced):
        """
        Fill the HTML_Table object with each child of the node.
        """
        pass

    def is_separate_node(self):
        """
        Return if the node is a separate node in the graph.
        """
        return not self.get_type() in config.no_reference_types

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        return self.get_type_name()
    
def is_separate_node(data):
    return isinstance(data, Node) and data.is_separate_node()
