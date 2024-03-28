from memory_graph.Node import Node
from memory_graph.Slicer import Slicer

import memory_graph.config_helpers as config_helpers

import math

def add_name_or_index(html_table, index, names):
    if names and index < len(names):
        html_table.add_entry(None, names[index], rounded=True)
    else:
        html_table.add_index(index)

class Node_Table(Node):

    def __init__(self, data, children, data_width=None, row_names=None, column_names=None):
        slicer_height, slicer_width = config_helpers.get_slicer_2d(self, data)

        if data_width:
            sliced_children = slicer_height.slice_2d(children, data_width)
            self.data_width = data_width
        else:
            sliced_children = slicer_height.slice(children)
            self.data_width = len(children[0])
        sliced_children.transform(lambda c: slicer_width.slice(c) )
        self.data_height = sliced_children.get_original_length()

        self.row_names = row_names
        self.column_names = column_names
        super().__init__(data, sliced_children, f'{self.data_height}⨯{self.data_width}')

    def transform(self, fun):
        self.children.transform(lambda s: s.transform(fun))

    def fill_html_table(self, html_table):
        # index on top row
        for index1, jump1, slice in self.children:
            if slice:
                html_table.add_value('', border=0)
                for index2, jump2, value in slice:
                    if jump2:
                        html_table.add_value('', border=0)
                    if value is not None:
                        add_name_or_index(html_table, index2, self.column_names)
                        #html_table.add_index(index2)
                html_table.add_new_line()
                break
        # remaining rows
        for index1, jump1, slice in self.children:
            #print('index1:',index1,'jump1:',jump1,'sliced:',slice)
            if jump1:
                html_table.add_new_line()
                html_table.add_value('', border=0)
                for _ in range (html_table.get_max_column()-1):
                    html_table.add_dots()
                html_table.add_new_line()
            if slice:
                add_name_or_index(html_table, index1, self.row_names)
                #html_table.add_index(index1)
                for index2, jump2, value in slice:
                    #print('  index2:',index2,'jump2:',jump2,'value:',value)
                    if jump2:
                        html_table.add_dots()
                    if value is not None:
                        html_table.add_entry(self, value)
                html_table.add_new_line()

