from Node import Node
from Slicer import Slicer
import config_helpers

class Node_Linear(Node):

    def __init__(self, data, children=None):
        slicer = config_helpers.get_slicer_1d(self, data)
        sliced_children = slicer.slice(children)
        super().__init__(data, sliced_children, len(children))

    def transform(self, fun):
        self.children.transform(fun)
        self.children.check_has_nodes()
        
    def fill_html_table(self, html_table):
        vertical = config_helpers.get_vertical_orientation(self, not self.children.has_node())
        if vertical:
            self.fill_html_table_vertical(html_table)
        else:
            self.fill_html_table_horizontal(html_table)

    def fill_html_table_vertical(self, html_table):
        for index, jump, value in self.children:
            if jump:
                html_table.add_entry(self, '', border=0)
                html_table.add_dots()
                html_table.add_new_line()
            if value:
                html_table.add_entry(self, index, border=0)
                html_table.add_entry(self, value)
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table):
        for index, jump, value in self.children:
            if jump:
                html_table.add_entry(self, '', border=0)
            if value:
                html_table.add_entry(self, index, border=0)
        html_table.add_new_line()
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots()
            if value:
                html_table.add_entry(self, value)

    