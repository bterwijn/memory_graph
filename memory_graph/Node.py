import memory_graph.utils as utils

class Node:
    """
    Node represents a node in the memory graph. This base class has different subclasses for different types of nodes.
    """

    node_id = 0
    
    """
    Create a Node object.

    Args:
        data (object): The data represented by the node.
        children (list): The children of the node.
        size (string): The size of the node to be shown in the graph.
    """
    def __init__(self, data, children=None):
        self.node_id = Node.node_id
        Node.node_id += 1
        self.data = data
        self.parent = None
        self.children = children

    def __repr__(self):
        """
        Return a string representation of the node showing the original data represented by the node.
        """
        return f'Node({self.data})'

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

    def set_parent(self, parent):
        """
        Set the parent of the node.
        """
        self.parent = parent

    def get_parent(self):
        """
        Return the parent of the node.
        """    
        return self.parent

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
        return f'node{self.node_id}'
    
    def get_html_table(self):
        """
        Return the HTML_Table object that determines how the node is visualized in the graph.
        """
        from memory_graph.HTML_Table import HTML_Table
        html_table = HTML_Table()
        if self.children is None:
            html_table.add_string(f'{self.data}')
        elif self.children.has_data():
            self.fill_html_table(html_table)
        return html_table
    
    # -------------------- Node interface, overriden by subclasses --------------------

    def do_backtrack_callback(self):
        """
        Returns if the callback function is called for this Node type. 
        """
        return True
    
    def transform(self, fun):
        """
        Transform each child of the node using the given 'fun' function. 
        This converts each child from raw data to a Node object.
        """
        pass
        
    def fill_html_table(self, html_table):
        """
        Fill the HTML_Table object with each child of the node.
        """
        pass

    def get_label(self):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        return self.get_type_name()