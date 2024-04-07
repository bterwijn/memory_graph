from memory_graph.Node import Node 

import memory_graph.config as config

import html

def outer_html_table(s, border, color):
    """ Helper function to add the outer HTML table tags to the string s setting the 'border' and 'color'. """
    return (f'<\n<TABLE BORDER="0" CELLBORDER="{border}" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="table">\n' +
            s + '\n</TD></TR></TABLE>\n>')

def inner_html_table(s):
    """ Helper function to add the innner HTML table tags to the string s. """
    return ('  <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5" CELLPADDING="0">\n    <TR>' +
            s + '</TR>\n  </TABLE>')

def format_string(s):
    """ Helper function to format the string s to be shown in the graph. Setting the max_string_length and escaping html characters. """
    if not type(s) is str:
        s = str(s)
    s = (s[:config.max_string_length] + '...') if len(s) > config.max_string_length else s
    return html.escape(s)

class HTML_Table:
    """
    The HTML_Table class is used to create a table of data that can be visualized in the graph.
    """
    
    def __init__(self):
        """
        Create an HTML_Table object.
        """
        self.html = ''
        self.add_new_line_flag = False
        self.col_count = 0
        self.row_count = 0
        self.ref_count = 0
        self.max_col_count = 0
        self.edges = []

    def __repr__(self):
        """ Get the string representation of the HTML_Table object. """
        return self.html

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
            self.html += '</TR>\n    <TR>'
            self.add_new_line_flag = False

    def add_string(self, s):
        """ Add a string s to the outer table. """
        self.html += format_string(s)
        #self.col_count += 1

    def add_index(self, s):
        """ Add an index s to the inner table. """
        self.check_add_new_line()
        self.html += f'<TD><font color="#505050">{str(s)}</font></TD>'
        self.col_count += 1

    def add_entry(self, node, child, rounded=False, border=1):
        """ Add child to the inner table either as reference if it a Node or as a value otherwise. """
        if isinstance(child, Node): 
            self.add_reference(node, child, rounded, border)
        else:
            self.add_value(child, rounded, border)

    def add_value(self, s, rounded=False, border=1):
        """ Helper function to add a value s to the inner table. """
        self.check_add_new_line()
        r = ' STYLE="ROUNDED"' if rounded else ''
        self.html += f'<TD BORDER="{border}"{r}> {format_string(s)} </TD>'
        self.col_count += 1

    def add_reference(self, node, child, rounded=False, border=1):
        """ Helper function to add a reference to the inner table. """
        self.check_add_new_line()
        r = ' STYLE="ROUNDED"' if rounded else ''
        self.html += f'<TD BORDER="{border}" PORT="ref{self.ref_count}"{r}> </TD>'
        self.edges.append( (f'{node.get_name()}:ref{self.ref_count}',
                            child.get_name()) )
        self.ref_count += 1
        self.col_count += 1

    def add_dots(self, rounded=False, border=1):
        """ Helper function to add dots to the inner table. """
        self.check_add_new_line()
        r = 'STYLE="ROUNDED"' if rounded else ''
        self.html += f'<TD BORDER="{border}" {r}>...</TD>'
        self.col_count += 1

    def to_string(self, border=1, color='white'):
        """ Construct the HTML table string with the 'border' and 'color' settings. """
        if self.col_count != 0 or self.row_count != 0:
            self.html = inner_html_table(self.html)
        if len(self.html) == 0:
            self.html = ' '
        return outer_html_table(self.html, border, color)
    
    def get_column(self):
        """ Get the number of columns in the inner table. """
        return self.col_count
    
    def get_max_column(self):
        """ Get the maximum value of the number of columns of rows in the inner tables. """
        return self.max_col_count
    
    def get_row(self):
        """ Get the number of rows in the inner table. """
        return self.row_count

    def get_edges(self):
        """ Get the edges that need to be acced t connect the table to other tables in the graph. """
        return self.edges

if __name__ == '__main__':
    table = HTML_Table()
    rows = 4
    columns = 5
    for r in range(rows):
        for c in range(columns):
            table.add_column(f'{c},{r}')
        table.add_new_line()
    print(table)
