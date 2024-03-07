import utils

def make_subgraph(children):
    child_names = [(c.set_subgraphed()).get_node_name()+':X' for c in children if not type(c) == str and not c.is_subgraphed()]
    if len(child_names) > 1:
        return '{ rank="same"  '+(" -> ".join(child_names))+'  [weight=99,style=invis]; }\n'
    return None

def outer_table(s):
    return ('<\n<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="blue"><TR><TD PORT="X">\n' +
            s +
            '\n</TD></TR></TABLE>\n>')

def inner_table(s):
    return ('<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="4" CELLPADDING="0"><TR>\n' +
            s +
            '\n</TR></TABLE>')

def get_node_and_edges_singular(categorized):
    return outer_table(str(categorized.get_data())), []

def get_node_and_edges_linear(categorized):
    edges = []
    if len(categorized.get_children()) == 0:
        node= outer_table(' ')
    else:
        node_name = categorized.get_node_name()
        s = ''
        for i,c in enumerate(categorized.get_children()):
            field=f'f{i}'
            if type(c) == str:
                 s += f'<TD>{c}</TD>'
            else:
                s += f'<TD PORT="{field}"> </TD>'
                edges.append( (node_name+':'+field, c.get_node_name()+':X') )
        node = outer_table(inner_table( s ))
    return node, edges

def get_node_and_edges_key_value(categorized):
    return get_node_and_edges_linear(categorized)
