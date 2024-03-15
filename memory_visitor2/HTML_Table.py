import html
import config 

def outer_html_table(s, border, color):
    return (f'<\n<TABLE BORDER="0" CELLBORDER="{border}" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X">\n' +
            s + '\n</TD></TR></TABLE>\n>')

def inner_html_table(s):
    return ('  <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5" CELLPADDING="0">\n    <TR>' +
            s + '</TR>\n  </TABLE>')

def format_string(s):
    s = (s[:config.max_string_length] + '..') if len(s) > config.max_string_length else s
    return html.escape(s)

class HTML_Table:

    def __init__(self):
        self.html = ''
        self.has_inner_table_flag = False
        self.add_new_line_flag = False
        self.ref_count=0
        self.edges = []

    def add_new_line(self):
        self.add_new_line_flag = True

    def check_add_new_line(self):
        if self.add_new_line_flag:
            self.html += '</TR>\n    <TR>'
            self.add_new_line_flag = False

    def add_inner_table(self):
        self.has_inner_table_flag = True

    def add_string(self, s):
        self.html += format_string(s)

    def add_column(self, s, rounded=False):
        self.check_add_new_line()
        r = ''
        if rounded:
            r = 'STYLE="ROUNDED"'
        self.html += f'<TD {r}> {format_string(s)} </TD>'

    def add_reference(self, node, child, rounded=False):
        self.check_add_new_line()
        r = ''
        if rounded:
            r = 'STYLE="ROUNDED"'
        self.html += f'<TD PORT="f{self.ref_count}" {r}> </TD>'
        self.edges.append( (f'{node.get_name()}:f{self.ref_count}',
                            f'{child.get_name()}:X') )
        self.ref_count+=1

    def add_dots(self):
        self.check_add_new_line()
        self.html += '<TD>...</TD>'

    def to_string(self, border=1, color='white'):
        if self.has_inner_table_flag:
            self.html = inner_html_table(self.html)
        return outer_html_table(self.html, border, color)
    
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
