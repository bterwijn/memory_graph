from Node import Node
from Slicer import Slicer
import config_helpers
import math
    
class Node_Table(Node):

    def __init__(self, data, children, data_width=None, column_names=None, row_names=None):
        slicer_height, slicer_width = config_helpers.get_slicer_2d(self, data)
        print('slicer_height:',slicer_height)
        print('slicer_width:',slicer_width)
        if data_width:
            sliced_children = slicer_height.slice_2d(children, data_width)
        else:
            sliced_children = slicer_height.slice(children)
        
        sliced_children.transform(lambda c: slicer_width.slice(c) )
        
        print('sliced_children:',sliced_children)

        # children_sliced = slicer_height.slice(children_sliced,3)
        # if column_names:
        #     self.column_names = (column_names + [' ']*(self.data_width-len(column_names)))[:self.data_width]
        #     self.column_names = slicer_width.slice(self.column_names)
        # if row_names:
        #     self.row_names = (row_names + [' ']*(self.data_height-len(row_names)))[:self.data_height]
        #     self.row_names = slicer_height.slice(self.row_names)


        self.data_height = sliced_children.get_original_length()
        slices = sliced_children.get_slices()
        print('slices:',slices)
        self.data_width = 3 #slices[0].get_data().get_original_length() if len(slices) > 0 else 0 # TODO
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
                    if value:
                        html_table.add_index(index2)
                html_table.add_new_line()
                break
        # remaining rows
        for index1, jump1, slice in self.children:
            print('index1:',index1,'jump1:',jump1,'sliced:',slice)
            if jump1:
                html_table.add_new_line()
                html_table.add_value('', border=0)
                for _ in range (html_table.get_max_column()-1):
                    html_table.add_dots()
                html_table.add_new_line()
            if slice:
                html_table.add_index(index1)
                for index2, jump2, value in slice:
                    print('  index2:',index2,'jump2:',jump2,'value:',value)
                    if jump2:
                        html_table.add_dots()
                    if value:
                        html_table.add_entry(self, value)
                html_table.add_new_line()