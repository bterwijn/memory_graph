# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph.config as config
import memory_graph.config_helpers as config_helpers
import memory_graph.utils as utils

def format_string(value, quote_str):
    """ Helper function to format 'value' to be shown in the graph. We escape html characters and convert newlines to <BR/> tags. """
    to_string = config_helpers.get_to_string(value)
    s = to_string(value)
    if quote_str and isinstance(value, (str, utils.full_str)):
        s = utils.quote_string(s)
    if not isinstance(value, utils.html_str): # <IMG> can't have padding in Graphviz
        s = utils.pad_string(s)
    return s

class HTML_Table:
    """
    The HTML_Table class is used to create a table of data that can be visualized in the graph.
    """
    
    def __init__(self):
        """
        Create an HTML_Table object.
        """
        self.rows = [[]]
        self.add_new_line_flag = False
        self.is_empty = True
        self.col_count = 0
        self.row_count = 0
        self.ref_count = 0
        self.max_col_count = 0
        self.edges = []
        self.rows_reversed = False
        self.columns_reversed = False

    def __repr__(self):
        """ Get the string representation of the HTML_Table object. """
        return str(self.rows)

    def add_row(self):
        self.rows.append([])

    def add_column(self, s):
        self.rows[-1].append(s)

    def reverse_rows(self, reversed=True):
        self.rows_reversed = reversed

    def reverse_columns(self, reversed=True):
        self.columns_reversed = reversed

    def add_new_line(self):
        """ Set the 'add_new_line_flag' to add a new line to the table when adding the next table element. """
        self.add_new_line_flag = True
        self.row_count += 1
        if self.col_count > self.max_col_count:
            self.max_col_count = self.col_count
        self.col_count = 0

    def check_add_new_line(self):
        """ Check if a new line should be added to the table, and if so add it and sets the 'add_new_line_flag' to False."""
        if self.add_new_line_flag:
            self.add_row()
            self.add_new_line_flag = False

    def add_index(self, s):
        """ Add an index s to the table. """
        self.check_add_new_line()
        self.add_column(f'<TD BORDER="0"><font color="{config.index_color}">{str(s)}</font></TD>')
        self.col_count += 1

    def add_entry(self, node, nodes, child, id_to_slices, rounded=False, border=1, dashed=False, embed=False):
        """ Add child to the table either as reference if it is a Node_Base or as a value otherwise. """
        child_id = id(child)
        if not embed and child_id in nodes:
            child = nodes[child_id] 
            if child_id in id_to_slices:
                self.add_reference(node, child, rounded, border, dashed)
            else:
                self.add_value(utils.unquoted_str(config.graph_cut_symbol), rounded, border)
        else:
            self.add_value(child, rounded, border)

    def add_value(self, value, rounded=False, border=1):
        """ Helper function to add 'value' to the table. """
        self.check_add_new_line()
        r = ' STYLE="ROUNDED"' if rounded else ''
        self.add_column(f'<TD BORDER="{border}"{r}>{format_string(value, not rounded)}</TD>')
        self.is_empty = False
        self.col_count += 1

    def add_reference(self, node, child, rounded=False, border=1, dashed=False):
        """ Helper function to add a reference to the table. """
        self.check_add_new_line()
        r = ' STYLE="ROUNDED"' if rounded else ''
        self.add_column(f'<TD BORDER="{border}" PORT="ref{self.ref_count}"{r}> </TD>')
        self.edges.append( (f'{node.get_name()}:ref{self.ref_count}',
                            child.get_name(), dashed) )
        self.ref_count += 1
        self.col_count += 1

    def add_dots(self, rounded=False, border=1):
        """ Helper function to add dots to the table. """
        self.check_add_new_line()
        r = 'STYLE="ROUNDED"' if rounded else ''
        self.add_column(f'<TD BORDER="{border}" {r}>...</TD>')
        self.col_count += 1

    def html_table_frame(self, border, color, line_color='black', spacing=5):
        """ Helper function to add the HTML table frame to the string s setting the 'border' and 'color'. """
        s = f'<\n<TABLE BORDER="{border}" CELLBORDER="1" CELLSPACING="{spacing}" CELLPADDING="0" BGCOLOR="{color}" COLOR="{line_color}" PORT="table">\n'
        s += ''.join('<TR>' + ''.join(cell for cell in (reversed(row) if self.columns_reversed else row)) + '</TR>\n' 
                for row in (reversed(self.rows) if self.rows_reversed else self.rows))
        s += '</TABLE>\n>'
        return s

    def to_string(self, border=1, color='white', line_color='black'):
        """ Construct the HTML table string with the 'border' and 'color' settings. """
        if self.col_count == 0 and self.row_count == 0:
            if self.is_empty:
                self.add_value(utils.unquoted_str(''), border=0)
            return self.html_table_frame(border, color, line_color, spacing=0)
        return self.html_table_frame(border, color, line_color)

    def get_column(self):
        """ Get the number of columns in the table. """
        return self.col_count
    
    def get_max_column(self):
        """ Get the maximum value of the number of columns of rows in the table. """
        return self.max_col_count
    
    def get_row(self):
        """ Get the number of rows in the table. """
        return self.row_count

    def get_edges(self):
        """ Get the edges that need to be added to connect the table to other tables in the graph. """
        return self.edges

if __name__ == '__main__':
    table = HTML_Table()
    rows = 4
    columns = 5
    #table.reverse_columns()
    for r in range(rows):
        for c in range(columns):
            table.add_value(f'{c},{r}')
        table.add_new_line()
    print(table.to_string())
