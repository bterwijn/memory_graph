from Node import Node
from Slicer import Slicer
import config_helpers
import math
    
class Node_Table(Node):

    def __init__(self, data, children, data_width=None, column_names=None, row_names=None):
        slicer_width, slicer_height = config_helpers.get_slicer_2d(self, data)
        print('slicer_width:',slicer_width)
        print('slicer_height:',slicer_height)
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


        self.data_height = 10
        self.data_width = 11
        #sliced_children = slicer_width.slice([i for i in range(20)])
        super().__init__(data, sliced_children, f'{self.data_height}⨯{self.data_width}')

    def transform(self, fun):
        self.children.transform(lambda s: s.transform(fun))

    def fill_html_table(self, html_table):
       dot_line = False
       for index1, jump1, sliced in self.children:
            print('index1:',index1,'jump1:',jump1,'sliced:',sliced)
            if jump1:
                dot_line = True
            if sliced:
                if html_table.get_row() == 0:  # first row
                    if html_table.get_column() == 0:
                        html_table.add_value('', border=0)
                    for index2, jump2, value in sliced:
                        if jump2:
                            html_table.add_value('', border=0)
                        if value:
                            html_table.add_index(index2)
                    html_table.add_new_line()

                if dot_line: # dot line
                    html_table.add_new_line()
                    html_table.add_value('', border=0)
                    for _ in range (html_table.get_max_column()-1):
                        html_table.add_dots()
                    html_table.add_new_line()
                    dot_line = False

                html_table.add_index(index1) # other rows
                for index2, jump2, value in sliced:
                    print('  index2:',index2,'jump2:',jump2,'value:',value)
                    if jump2:
                        html_table.add_dots()
                    if value:
                        html_table.add_entry(self, value)
                html_table.add_new_line()