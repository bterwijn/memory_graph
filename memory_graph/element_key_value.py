from memory_graph.element_base import Element_Base
from memory_graph.sequence import Sequence1D

import memory_graph.config_helpers as config_helpers

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
    
    def has_references(self, slices, sliced_elements):
        """
        Return if the node has references to other nodes.
        """
        for index in slices:
            child = self.children[index]
            key = child.get_children()[0]
            if key.is_node() and not key.is_hidden_node():
                return True
            value = child.get_children()[1]
            if value.is_node() and not value.is_hidden_node():
                return True
        return False

    def is_vertical(self, slices, sliced_elements):
        """
        Return if the node is vertical or horizontal based on the orientation of the children.
        """
        vertical = config_helpers.get_vertical_orientation(self, None)
        if vertical is None:
            vertical = not self.has_references(slices, sliced_elements)
        return vertical

    def fill_html_table(self, html_table, slices, sliced_elements):
        """
        Fill the html_table with the children of the Element_Base.
        """
        vertical = self.is_vertical(slices, sliced_elements)
        if vertical:
            self.fill_html_table_vertical(html_table, slices, sliced_elements)
        else:
            self.fill_html_table_horizontal(html_table, slices, sliced_elements)

    @staticmethod
    def get_value_dashed(child, index):
        value = child.get_children()[index]
        is_dashed = False
        #if child_id in graph_sliced.get_node_ids():
        #    is_dashed = graph_sliced.get_slices(child_id).is_dashed(index)
        return value, is_dashed

    def fill_html_table_vertical(self, html_table, slices, sliced_elements):
        """
        Helper function to fill the html_table with the children of the Element_Base in vertical orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                key, is_dashed = self.get_value_dashed(child,0)
                html_table.add_entry(self, key, sliced_elements, rounded=True, dashed=is_dashed)
                value, is_dashed = self.get_value_dashed(child,1)
                html_table.add_entry(self, value, sliced_elements, dashed=is_dashed)
            else:
                html_table.add_dots()
                html_table.add_dots()
            html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, slices, sliced_elements):
        """
        Helper function to fill the html_table with the children of the Element_Base in horizontal orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                key, is_dashed = self.get_value_dashed(child,0)
                html_table.add_entry(self, key, sliced_elements, rounded=True, dashed=is_dashed)
            else:
                html_table.add_dots()
        html_table.add_new_line()
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                value, is_dashed = self.get_value_dashed(child,1)
                html_table.add_entry(self, value, sliced_elements, dashed=is_dashed)
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