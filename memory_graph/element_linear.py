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
    
    def has_references(self, slices, graph_sliced):
        """
        Return if the node has references to other nodes.
        """
        for index in slices:
            if id(self.children[index]) in graph_sliced.node_ids:
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
        if self.is_vertical(slices, graph_sliced):
            self.fill_html_table_vertical(html_table, slices, graph_sliced)
        else:
            self.fill_html_table_horizontal(html_table, slices, graph_sliced)

    def fill_html_table_vertical(self, html_table, slices, graph_sliced):
        """
        Helper function to fill the html_table with the children of the Element_Base in vertical orientation.
        """
        children = self.children
        graph_full = graph_sliced.get_graph_full()
        for index in slices.table_iter(children.size()):
            if index>=0:
                html_table.add_index(index)
                child = graph_full.get_element(children[index])
                html_table.add_entry(self, child, graph_sliced, dashed=slices.is_dashed(index))
                html_table.add_new_line()
            else:
                html_table.add_value('', border=0)
                html_table.add_dots()
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table, slices, graph_sliced):
        """
        Helper function to fill the html_table with the children of the Element_Base in horizontal orientation.
        """
        children = self.children
        graph_full = graph_sliced.get_graph_full()
        for index in slices.table_iter(children.size()):
            if index>=0:
                html_table.add_index(index)
            else:
                html_table.add_value('', border=0)
        html_table.add_new_line()
        for index in slices.table_iter(children.size()):
            if index>=0:
                child = graph_full.get_element(children[index])
                html_table.add_entry(self, child, graph_sliced, dashed=slices.is_dashed(index))
            else:
                html_table.add_dots()

    def is_node(self):
        return True

    def get_label(self, slices):
        """
        Return a label for the node to be shown in the graph next to the HTML table.
        """
        type_name = self.get_type_name()
        s = slices.get_slices()
        if len(s) > 0:
            last_index = s[-1][1]
            size = self.get_children().size()
            if last_index != size:
                return f'{type_name} {size}'
        return f'{type_name}'
        