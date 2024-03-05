from functools import singledispatch
import utils

def make_subgraph(children):
    return '{ rank="same"  '+(" -> ".join(children))+'  [weight=99,style=invis]; }\n'

def outer_table(s):
    return ('<\n<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="blue"><TR><TD PORT="X">\n' +
            s +
            '\n</TD></TR></TABLE>\n>')

def inner_table(s):
    return ('<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="4" CELLPADDING="0"><TR>\n' +
            s +
            '\n</TR></TABLE>')

def make_singular_body(categorized):
    return outer_table( 
            str(categorized.get_data()) 
            )

def make_linear_body(categorized):
    s = ''
    for i,c in enumerate(categorized.get_children()):
        s += f'<TD PORT="f{i}"> </TD>'
    return outer_table(
            inner_table( 
                s
            ))