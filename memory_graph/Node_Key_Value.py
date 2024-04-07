from memory_graph.Node import Node
from memory_graph.Node_Hidden import Node_Hidden
from memory_graph.Slicer import Slicer

import memory_graph.config_helpers as config_helpers
import memory_graph.utils as utils

def transform_node_hidden(node_hidden, fun):
    """
    Helper function to forward the transform to the children of the Node_Hidden node.
    """
    node_hidden.transform(fun)
    return node_hidden

def hidden_has_nodes(node_hidden):
    """
    Helper function to check if the Node_Hidden node has any children that are Node 
    objects so that references need to be drawn in the graph.
    """
    for c in node_hidden.get_children():
        if isinstance(c, Node):
            return True
    return False

class Node_Key_Value(Node):
    """
    Node_Key_Value (subclass of Node) is a node that represents a node with key-value 
    pairs (tuples) as children. This node type mainly used for dictionaries and classes. 
    Each child is made a Hidden_Node so that each tuple is not shown as a separate node 
    but instead as a key,value pair in the current node.
    """

    def __init__(self, data, children):
        """
        Create a Node_Key_Value object. Use a Slicer to slice the children so the
        Node will not get too big or have too many childeren in the graph.
        """
        #print('Node_Key_Value children:', children)
        hidden_children = [ Node_Hidden(i,list(i)) for i in children ]
        slicer = config_helpers.get_slicer_1d(self, data)
        sliced_children = slicer.slice(hidden_children)
        super().__init__(data, sliced_children, sliced_children.get_original_length())
        
    def transform(self, fun):
        """
        Transform the children of the Node using the 'fun' function and the 
        'transform_node_hidden' helper to function transform each key and value instead of each tuple.
        """
        self.children.transform(lambda node_hidden: transform_node_hidden(node_hidden, fun) )
        
    def fill_html_table(self, html_table):
        """
        Fill the html_table with the children of the Node.
        """
        has_nodes = self.children.check_condition_on_children(lambda c: hidden_has_nodes(c))
        vertical = config_helpers.get_vertical_orientation(self, not has_nodes)
        if vertical:
            self.fill_html_table_vertical(html_table)
        else:
            self.fill_html_table_horizontal(html_table)

    def fill_html_table_vertical(self, html_table):
        """
        Helper function to fill the html_table with the children of the Node in vertical orientation.
        """
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots(rounded=True)
                html_table.add_dots()
                html_table.add_new_line()
            if value is not None:
                key_value = value.get_children() # add the key-value pair of Hidden_Node, not the tuple
                html_table.add_entry(self, key_value[0], rounded=True)
                html_table.add_entry(self, key_value[1])
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table):
        """
        Helper function to fill the html_table with the children of the Node in horizontal orientation.
        """
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots(rounded=True)
            if value is not None:
                key_value = value.get_children() # add the key-value pair of Hidden_Node, not the tuple
                html_table.add_entry(self, key_value[0], rounded=True)
        html_table.add_new_line()
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots()
            if value is not None:
                key_value = value.get_children() # add the key-value pair of Hidden_Node, not the tuple
                html_table.add_entry(self, key_value[1])
