from memory_graph.element_base import Element_Base
from memory_graph.sequence import Sequence1D

import memory_graph.config_helpers as config_helpers

def transform_node_hidden(node_hidden, fun):
    """
    Helper function to forward the transform to the children of the Element_Hidden node.
    """
    node_hidden.transform(fun)
    return node_hidden

def hidden_has_nodes(node_hidden):
    """
    Helper function to check if the Element_Hidden node has any children that are Element_Base 
    objects so that references need to be drawn in the graph.
    """
    for c in node_hidden.get_children():
        if isinstance(c, Element_Base):
            return True
    return False

class Element_Key_Value(Element_Base):
    """
    Element_Key_Value (subclass of Element_Base) is a node that represents a node with key-value 
    pairs (tuples) as children. This node type mainly used for dictionaries and classes. 
    Each child is made a Hidden_Element_Base so that each tuple is not shown as a separate node 
    but instead as a key,value pair in the current node.
    """

    def __init__(self, data, children):
        """
        Create a Element_Key_Value object. Use a Slicer to slice the children so the
        Element_Base will not get too big or have too many childeren in the graph.
        """
        super().__init__(data, Sequence1D(children))
        
    def transform(self, fun):
        """
        Transform the children of the Element_Base using the 'fun' function and the 
        'transform_node_hidden' helper to function transform each key and value instead of each tuple.
        """
        self.children.transform(lambda node_hidden: transform_node_hidden(node_hidden, fun) )
    
    def has_references(self, slices, graph_sliced):
        """
        Return if the node has references to other nodes.
        """
        graph_full = graph_sliced.get_graph_full()
        for index in slices:
            child = graph_full.get_element(self.children[index])
            key = child.get_children()[0]
            if id(key) in graph_sliced.get_node_ids():
                return True
            value = child.get_children()[1]
            if id(value) in graph_sliced.get_node_ids():
                return True
        return False

    def is_vertical(self, slices, graph_sliced):
        """
        Return if the node is vertical or horizontal based on the orientation of the children.
        """
        vertical = config_helpers.get_vertical_orientation(self, None)
        if vertical is None:
            vertical = not self.has_references(slices, graph_sliced)
        return vertical

    def fill_html_table(self, html_table, slices, graph_sliced):
        """
        Fill the html_table with the children of the Element_Base.
        """
        vertical = self.is_vertical(slices, graph_sliced)
        if vertical:
            self.fill_html_table_vertical(html_table, slices, graph_sliced)
        else:
            self.fill_html_table_horizontal(html_table, slices, graph_sliced)

    @staticmethod
    def get_value_dashed(child_id, index, graph_sliced):
        graph_full = graph_sliced.get_graph_full()
        child = graph_full.get_element_by_id(child_id)
        value = graph_full.get_element_by_id(id(child.get_children()[index]))
        is_dashed = False
        if child_id in graph_sliced.get_node_ids():
            is_dashed = graph_sliced.get_slices(child_id).is_dashed(index)
        return value, is_dashed

    def fill_html_table_vertical(self, html_table, slices, graph_sliced):
        """
        Helper function to fill the html_table with the children of the Element_Base in vertical orientation.
        """
        children = self.children
        graph_full = graph_sliced.get_graph_full()
        for index in slices.table_iter(children.size()):
            if index>=0:
                key, is_dashed = self.get_value_dashed(id(children[index]),0,graph_sliced)
                html_table.add_entry(self, key, graph_sliced, rounded=True, dashed=is_dashed)
                value, is_dashed = self.get_value_dashed(id(children[index]),1,graph_sliced)
                html_table.add_entry(self, value, graph_sliced, dashed=is_dashed)
            else:
                html_table.add_dots()
                html_table.add_dots()
            html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, slices, graph_sliced):
        """
        Helper function to fill the html_table with the children of the Element_Base in horizontal orientation.
        """
        children = self.children
        for index in slices.table_iter(children.size()):
            if index>=0:
                key, is_dashed = self.get_value_dashed(id(children[index]),0,graph_sliced)
                html_table.add_entry(self, key, graph_sliced, rounded=True, dashed=is_dashed)
            else:
                html_table.add_dots()
        html_table.add_new_line()
        for index in slices.table_iter(children.size()):
            if index>=0:
                value, is_dashed = self.get_value_dashed(id(children[index]),1,graph_sliced)
                html_table.add_entry(self, value, graph_sliced, dashed=is_dashed)
            else:
                html_table.add_dots()

    def is_node(self):
        return True

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        type_name = self.get_type_name()
        size = self.get_children().size()
        s = slices.get_slices()
        if len(s) == 1:
            if s[0][1] - s[0][0] == size:
                return f'{type_name}'
        return f'{type_name} {size}'