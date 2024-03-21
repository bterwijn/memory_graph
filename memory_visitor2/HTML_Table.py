import html
import config 
from Node import Node 

def outer_html_table(s, border, color):
    return (f'<\n<TABLE BORDER="0" CELLBORDER="{border}" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="table">\n' +
            s + '\n</TD></TR></TABLE>\n>')

def inner_html_table(s):
    return ('  <TABLE BORDER="0" CELLBORDER="0" CELLSPACING="5" CELLPADDING="0">\n    <TR>' +
            s + '</TR>\n  </TABLE>')

def format_string(s):
    if not type(s) is str:
        s = str(s)
    s = (s[:config.max_string_length] + '...') if len(s) > config.max_string_length else s
    return html.escape(s)

class HTML_Table:

    def __init__(self):
        self.html = ''
        self.has_inner_table_flag = False
        self.add_new_line_flag = False
        self.col_count = 0
        self.row_count = 0
        self.ref_count=0
        self.max_col_count = 0
        self.edges = []

    def __repr__(self):
        return self.html

    def add_new_line(self):
        self.add_new_line_flag = True
        self.row_count += 1
        if self.col_count > self.max_col_count:
            self.max_col_count = self.col_count
        self.col_count = 0

    def check_add_new_line(self):
        if self.add_new_line_flag:
            self.html += '</TR>\n    <TR>'
            self.add_new_line_flag = False

    def add_inner_table(self):
        self.has_inner_table_flag = True

    def add_string(self, s):
        self.html += format_string(s)
        self.col_count += 1

    def add_index(self, s):
        self.check_add_new_line()
        self.html += f'<TD><font color="#505050">{str(s)}</font></TD>'
        self.col_count += 1

    def add_entry(self, node, child, rounded=False, border=1):
        if isinstance(child, Node): 
            self.add_reference(node, child, rounded, border)
        else:
            self.add_value(child, rounded, border)

    def add_value(self, s, rounded=False, border=1):
        self.check_add_new_line()
        r = ' STYLE="ROUNDED"' if rounded else ''
        self.html += f'<TD BORDER="{border}"{r}> {format_string(s)} </TD>'
        self.col_count += 1

    def add_reference(self, node, child, rounded=False, border=1):
        self.check_add_new_line()
        r = ' STYLE="ROUNDED"' if rounded else ''
        self.html += f'<TD BORDER="{border}" PORT="ref{self.ref_count}"{r}> </TD>'
        self.edges.append( (f'{node.get_name()}:ref{self.ref_count}',
                            child.get_name()) )
        self.ref_count+=1
        self.col_count += 1

    def add_dots(self, rounded=False, border=1):
        self.check_add_new_line()
        r = 'STYLE="ROUNDED"' if rounded else ''
        self.html += f'<TD BORDER="{border}" {r}>...</TD>'
        self.col_count += 1

    def to_string(self, border=1, color='white'):
        if self.has_inner_table_flag:
            self.html = inner_html_table(self.html)
        return outer_html_table(self.html, border, color)
    
    def get_column(self):
        return self.col_count
    
    def get_max_column(self):
        return self.max_col_count
    
    def get_row(self):
        return self.row_count

    def get_edges(self):
        return self.edges

if __name__ == '__main__':
    table = HTML_Table()
    rows = 4
    columns = 5
    for r in range(rows):
        for c in range(columns):
            table.add_column(f'{c},{r}')
        table.add_new_line()
    table.add_inner_table()
    print(table)
