from memory_graph.element_base import Element_Base
from memory_graph.sequence import Sequence1D

import memory_graph.config_helpers as config_helpers

class Element_Linear(Element_Base):
    """
    Element_Linear (subclass of Element_Base) is a node that represents a linear sequence 
    of data used for most iterable type like list, tuple, set, etc.
    """

    def __init__(self, data, children=None):
        """
        Create a Element_Linear object. Use a Slicer to slice the children so the 
        Element_Base will not get to big or have too many childeren in the graph.
        """
        super().__init__(data, Sequence1D(children))
    
    def has_references(self, slices):
        """
        Return if the node has references to other nodes.
        """
        for index in slices:
            child = self.children[index]
            if child.is_node() and not child.is_hidden_node():
                return True
        return False

    def is_vertical(self, slices, sliced_elements):
        """
        Return if the node is vertical or horizontal based on the orientation of the children.
        """
        vertical = config_helpers.get_vertical_orientation(self, None)
        if vertical is None:
            vertical = not self.has_references(slices)
        return vertical

    def fill_html_table(self, html_table, slices, sliced_elements):
        """
        Fill the html_table with the children of the Element_Base.
        """
        if self.is_vertical(slices, sliced_elements):
            self.fill_html_table_vertical(html_table, slices, sliced_elements)
        else:
            self.fill_html_table_horizontal(html_table, slices, sliced_elements)

    def fill_html_table_vertical(self, html_table, slices, sliced_elements):
        """
        Helper function to fill the html_table with the children of the Element_Base in vertical orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                html_table.add_index(index)
                child = self.children[index]
                html_table.add_entry(self, child, sliced_elements, dashed=slices.is_dashed(index))
                html_table.add_new_line()
            else:
                html_table.add_value('', border=0)
                html_table.add_dots()
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, slices, sliced_elements):
        """
        Helper function to fill the html_table with the children of the Element_Base in horizontal orientation.
        """
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                html_table.add_index(index)
            else:
                html_table.add_value('', border=0)
        html_table.add_new_line()
        for index in slices.table_iter(self.children.size()):
            if index>=0:
                child = self.children[index]
                html_table.add_entry(self, child, sliced_elements, dashed=slices.is_dashed(index))
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
        