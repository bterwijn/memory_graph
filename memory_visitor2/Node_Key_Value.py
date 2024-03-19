from Node import Node
from Node_Hidden import Node_Hidden
from Slicer import Slicer
import config_helpers

def transform_node_hidden(node_hidden, fun):
    node_hidden.transform(fun)
    # node_hidden.check_has_nodes() # TODO
    return node_hidden

def hidden_has_nodes(node_hidden):
    for c in node_hidden.get_children():
        if isinstance(c, Node):
            return True
    return False

class Node_Key_Value(Node):

    def __init__(self, data, children):
        #print('Node_Key_Value children:', children)
        hidden_children = [Node_Hidden(i,list(i)) for i in children]
        slicer = config_helpers.get_slicer_1d(self, data)
        sliced_children = slicer.slice(hidden_children)
        super().__init__(data, sliced_children, len(hidden_children))
        
    def transform(self, fun):
        self.children.transform(lambda node_hidden:  transform_node_hidden(node_hidden, fun) )
        
    def fill_html_table(self, html_table):
        has_nodes = self.children.check_condition_on_children(lambda c: hidden_has_nodes(c))
        vertical = config_helpers.get_vertical_orientation(self, not has_nodes)
        if vertical:
            self.fill_html_table_vertical(html_table)
        else:
            self.fill_html_table_horizontal(html_table)

    def fill_html_table_vertical(self, html_table):
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots()
                html_table.add_dots()
                html_table.add_new_line()
            if value:
                key_value = value.get_children()
                html_table.add_entry(self, key_value[0])
                html_table.add_entry(self, key_value[1])
                html_table.add_new_line()

    def fill_html_table_horizontal(self, html_table):
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots()
            if value:
                key_value = value.get_children()
                html_table.add_entry(self, key_value[0])
        html_table.add_new_line()
        for index, jump, value in self.children:
            if jump:
                html_table.add_dots()
            if value:
                key_value = value.get_children()
                html_table.add_entry(self, key_value[1])
