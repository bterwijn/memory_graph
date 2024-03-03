
singular_categories = ['int','float','str','bool','NoneType']

def get_type_name(data):
    return type(data).__name__

def make_node_body(data,children):
    body = '<\n<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="blue"><TR><TD PORT="X">\n'
    if len(children) > 0:
        body += '  <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="4" CELLPADDING="0"><TR>\n'
        body += '     '
        for i,c in enumerate(children):
            body += f'<TD PORT="f{i}"> </TD>'
        body += '\n  </TR></TABLE>\n'
        pass
    elif get_type_name(data) in singular_categories:
        body += f'{data}\n'
    body += '</TD></TR></TABLE>>'
    return body

def make_subgraph(children):
    return '{ rank="same"  '+(" -> ".join(children))+'  [weight=99,style=invis]; }\n'
