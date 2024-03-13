import html

def outer_html_table(s, border, color):
    return (f'<\n<TABLE BORDER="0" CELLBORDER="{border}" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X">\n' +
            s + '\n</TD></TR></TABLE>\n>')

def inner_html_table(s):
    return ('  <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5" CELLPADDING="0">\n    <TR>' +
            s + '</TR>\n  </TABLE>')

class HTML_Table:

    def __init__(self):
        self.html = ''
        self.has_inner_table_flag = False
        self.add_new_line_flag = False

    def add_new_line(self):
        self.add_new_line_flag = True

    def check_add_new_line(self):
        if self.add_new_line_flag:
            self.html += '</TR>\n    <TR>'
            self.add_new_line_flag = False

    def add_inner_table(self):
        self.has_inner_table_flag = True

    def add_string(self, s):
        self.html += html.escape(s)

    def add_column(self, s):
        self.check_add_new_line()
        self.html += f'<TD> {html.escape(s)} </TD>'

    def add_dots(self):
        self.check_add_new_line()
        self.html += '<TD>...</TD>'

    def __repr__(self, border=1, color='white'):
        if self.has_inner_table_flag:
            self.html = inner_html_table(self.html)
        return outer_html_table(self.html, border, color)

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
