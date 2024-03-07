import memory_visitor
import categories
import utils

no_child_references_types = {utils.class_type, dict, }
no_child_references_types = {}

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

def add_to_graph_singular(categorized, graph):
        graph.node(categorized.get_node_name(),
                   outer_table(str(categorized.get_data())), 
                   xlabel=categorized.get_type_name())

def make_linear_body(categorized, graph):
    body = ''
    field_count = 0
    for c in categorized.get_children():
        if type(c) == str:
            body += f'<TD>{c}</TD>'
        else:
            field=f'f{field_count}'
            body += f'<TD PORT="{field}"> </TD>'
            graph.edge(f'{categorized.get_node_name()}:{field}', f'{c.get_node_name()}:X')
        field_count += 1
    return inner_table(body)

def add_to_graph_linear(categorized, graph):
    parent = categorized.get_parent()
    if parent and (type(parent.get_data()) in no_child_references_types or 
        parent.get_alternative_type() in no_child_references_types):
        return
    node_name = categorized.get_node_name()
    node_body = ''
    if len(categorized.get_children()) == 0:
        node_body = str(categorized.get_data())
    else:
        node_body = make_linear_body(categorized, graph)
    graph.node(node_name, 
               outer_table(node_body), 
               xlabel=categorized.get_type_name())

def make_key_value_body(categorized, graph):
    body = ''
    field_count = 0
    for c in categorized.get_children():
        for c2 in c.get_children():
            if type(c2) == str:
                body += f'<TD>{c2}</TD>'
            else:
                field=f'f{field_count}'
                body += f'<TD PORT="f{field_count}"> </TD>'
                graph.edge(f'{categorized.get_node_name()}:{field}', f'{c.get_node_name()}:X')
        field_count += 1
    return inner_table(body)

def add_to_graph_key_value(categorized, graph):
    node_name = categorized.get_node_name()
    node_body = ''
    if len(categorized.get_children()) == 0:
        node_body = str(categorized.get_data())
    else:
        if (type(categorized.get_data()) in no_child_references_types or
             categorized.get_alternative_type() in no_child_references_types):
            node_body = make_key_value_body(categorized, graph)
        else:
            node_body = make_linear_body(categorized, graph)
    graph.node(node_name, 
               outer_table(node_body), 
               xlabel=categorized.get_type_name())
