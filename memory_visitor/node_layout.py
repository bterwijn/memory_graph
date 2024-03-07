import memory_visitor
import categories
import utils

no_child_references_types = {utils.class_type, dict, }

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
    parent = categorized.get_parent()
    if parent and (type(parent.get_data()) in no_child_references_types or 
        parent.get_alternative_type() in no_child_references_types):
        return None, None
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
    edges = []
    if len(categorized.get_children()) == 0:
        node= outer_table(' ')
    else:
        node_name = categorized.get_node_name()
        s = ''
        field_count = 0

        if (type(categorized.get_data()) in no_child_references_types or
            categorized.get_alternative_type() in no_child_references_types):
            for c in categorized.get_children():
                for c2 in c.get_children():
                    if type(c2) == str:
                        s += f'<TD>{c2}</TD>'
                    else:
                        s += f'<TD PORT="f{field_count}"> </TD>'
                        edges.append( (f"node_name:f{field_count}", f"{c.get_node_name()}:X") )
                    field_count += 1
        else:
            for i,c in enumerate(categorized.get_children()):
                field=f'f{i}'
                if type(c) == str:
                    s += f'<TD>{c}</TD>'
                else:
                    s += f'<TD PORT="{field}"> </TD>'
                    edges.append( (node_name+':'+field, c.get_node_name()+':X') )
        node = outer_table(inner_table( s ))
    return node, edges