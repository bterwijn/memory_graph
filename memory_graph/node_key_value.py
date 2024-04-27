from memory_graph.node import Node
from memory_graph.sequence import Sequence1D


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
        super().__init__(data, Sequence1D(children))
        
    def transform(self, fun):
        """
        Transform the children of the Node using the 'fun' function and the 
        'transform_node_hidden' helper to function transform each key and value instead of each tuple.
        """
        self.children.transform(lambda node_hidden: transform_node_hidden(node_hidden, fun) )
        
    def fill_html_table(self, html_table, slices, full_graph):
        """
        Fill the html_table with the children of the Node.
        """
        #has_nodes = self.children.check_condition_on_children(lambda c: hidden_has_nodes(c))
        vertical = True #config_helpers.get_vertical_orientation(self, not has_nodes)
        if vertical:
            self.fill_html_table_vertical(html_table, slices, full_graph)
        else:
            self.fill_html_table_horizontal(html_table, slices, full_graph)

    def fill_html_table_vertical(self, html_table, slices, full_graph):
        """
        Helper function to fill the html_table with the children of the Node in vertical orientation.
        """
        children = self.children
        for index in slices.table_iter(children.size()):
            if index>=0:
                child = children[index]
                child_node = full_graph.get_child_node(child)
                key = full_graph.get_node(id(child_node.get_children()[0]))
                html_table.add_entry(self, key, rounded=True)
                value = full_graph.get_node(id(child_node.get_children()[1]))
                html_table.add_entry(self, value)
            else:
                html_table.add_dots()
                html_table.add_dots()
            html_table.add_new_line()

        # for index in slices.get_iter(self.get_nr_children()):
        #     if index == None:
        #         html_table.add_value('', border=0)
        #         html_table.add_dots()
        #         html_table.add_dots()
        #     else:
        #         html_table.add_index(index)
        #         child_node = full_graph.get_child(self.children, index)
        #         key = full_graph.get_node(id(child_node.get_children()[0]))
        #         html_table.add_entry(self, key)
        #         value = full_graph.get_node(id(child_node.get_children()[1]))
        #         html_table.add_entry(self, value)
        #     html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, slices, full_graph):
        """
        Helper function to fill the html_table with the children of the Node in horizontal orientation.
        """
        children = self.children
        for index in slices.table_iter(children.size()):
            if index>=0:
                child = children[index]
                child_node = full_graph.get_child_node(child)
                key = full_graph.get_node(id(child_node.get_children()[0]))
                html_table.add_entry(self, key, rounded=True)
            else:
                html_table.add_dots()
        html_table.add_new_line()
        for index in slices.table_iter(children.size()):
            if index>=0:
                child = children[index]
                child_node = full_graph.get_child_node(child)
                value = full_graph.get_node(id(child_node.get_children()[1]))
                html_table.add_entry(self, value)
            else:
                html_table.add_dots()

    def get_label(self):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        return f'{self.get_type_name()}'
        # if self.get_children().has_all_data():
        #     return f'{self.get_type_name()}'
        # return f'{self.get_type_name()} {self.size}'
    