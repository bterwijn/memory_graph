import utils

category_singular = {'bool','int','float','complex','str','NoneType'}
category_linear = {'tuple','list','set','frozenset'}
category_key_value = {'dict','mappingproxy'}
category_table = set()

def make_subgraph(children):
    return '{ rank="same"  '+(" -> ".join(children))+'  [weight=99,style=invis]; }\n'

def make_node_body_linear(category):
    body = '<\n<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="blue"><TR><TD PORT="X">\n'
    if len(category.get_children()) > 0:
        body += '  <TABLE BORDER="0" CELLBORDER="1" CELLSPACING="4" CELLPADDING="0"><TR>\n'
        body += '     '
        for i,c in enumerate(category.get_children()):
            body += f'<TD PORT="f{i}"> </TD>'
        body += '\n  </TR></TABLE>\n'
        pass
    elif category.get_type_name() in category_singular:
        body += f'{category.get_data()}\n'
    body += '</TD></TR></TABLE>>'
    return body

def make_node_body(category):
    return make_node_body_linear(category)
