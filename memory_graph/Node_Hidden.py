from memory_graph.Node import Node

class Node_Hidden(Node):
    """
    Node_Hidden (subclass of Node) is a node that represents a node that is not shown 
    in the graph. This is used for the children of Node_Key_Value to hide the separate 
    tuples Nodes and visualize the key-value pairs in the Node_Key_Value instead.
    """

    def __init__(self, data, children):
        """
        Create a Node_Hidden object.
        """
        super().__init__(data, children)

    def do_backtrack_callback(self):
        """
        Do not call the backtrack_callback function so that the Node_Hidden is not shown in the graph.
        """
        return False
    
    def transform(self, fun):
        """
        Transform the children of the Node using the 'fun' function.
        """
        self.children = [fun(i) for i in self.children]
