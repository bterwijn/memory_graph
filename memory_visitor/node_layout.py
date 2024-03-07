import memory_visitor
import categories
import utils

drop_child_references_types = {utils.class_type, dict, }
no_drop_child_references_types = set()

def drop_child_references(categorized):
    type1 = type(categorized.get_data())
    type2 = categorized.get_alternative_type()
    return ((type1 in drop_child_references_types or type2 in drop_child_references_types) and not
            (type1 in no_drop_child_references_types or type2 in no_drop_child_references_types))

def outer_table(s):
    return ('<\n<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="blue"><TR><TD PORT="X">\n' +
            s +
            '\n</TD></TR></TABLE>\n>')

def inner_table(s):
    return ('<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="4" CELLPADDING="0"><TR>\n' +
            s +
            '\n</TR></TABLE>')

class Subgraph:

    def __init__(self):
        self.children = []

    def add_child(self, child):
        if not child.is_subgraphed():
            child.set_subgraphed()
            self.children.append(f'{child.get_node_name()}:X')

    def add_subgraph(self, graph):
        if len(self.children) > 1:
            graph.body.append('{ rank="same"  '+(" -> ".join(self.children))+'  [weight=99,style=invis]; }\n')

def add_to_graph_singular(categorized, graph):
        graph.node(categorized.get_node_name(),
                   outer_table(str(categorized.get_data())),
                   xlabel=categorized.get_type_name())

def make_body(categorized, graph, fun):
    if len(categorized.get_children()) == 0:
        return str(categorized.get_data())
    return fun(categorized, graph)

def make_linear_body(categorized, graph):
    body = ''
    subgraph = Subgraph()
    field_count = 0
    for c in categorized.get_children():
        if type(c) == str:
            body += f'<TD>{c}</TD>'
        else:
            field=f'f{field_count}'
            body += f'<TD PORT="{field}"> </TD>'
            cname = f'{c.get_node_name()}:X'
            graph.edge(f'{categorized.get_node_name()}:{field}', cname)
            subgraph.add_child(c)
        field_count += 1
    subgraph.add_subgraph(graph)
    return inner_table(body)

def add_to_graph_linear(categorized, graph):
    parent = categorized.get_parent()
    if parent and drop_child_references(parent):
        return
    graph.node(categorized.get_node_name(),
               outer_table(make_body(categorized, graph, make_linear_body)),
               xlabel=categorized.get_type_name())

def make_key_value_body(categorized, graph):
    body = ''
    subgraph = Subgraph()
    field_count = 0
    for c1 in categorized.get_children():
        for c in c1.get_children():
            if type(c) == str:
                body += f'<TD>{c}</TD>'
            else:
                field=f'f{field_count}'
                body += f'<TD PORT="{field}"> </TD>'
                cname = f'{c.get_node_name()}:X'
                graph.edge(f'{categorized.get_node_name()}:{field}', cname)
                subgraph.add_child(c)
        field_count += 1
    subgraph.add_subgraph(graph)
    return inner_table(body)

def add_to_graph_key_value(categorized, graph):
    graph.node(categorized.get_node_name(),
               outer_table(make_body(categorized, graph, make_key_value_body)),
               xlabel=categorized.get_type_name())

def make_table_body(categorized, graph):
    nr_columns = categorized.get_size()[1]
    print('nr_columns:',nr_columns)
    body = ''
    subgraph = Subgraph()
    field_count = 0
    new_row = ''
    for c in categorized.get_children():
        body += new_row
        new_row = ''
        if type(c) == str:
            body += f'<TD>{c}</TD>'
        else:
            field=f'f{field_count}'
            body += f'<TD PORT="{field}"> </TD>'
            cname = f'{c.get_node_name()}:X'
            graph.edge(f'{categorized.get_node_name()}:{field}', cname)
            subgraph.add_child(c)
        if field_count%nr_columns == nr_columns-1:
            new_row = '</TR>\n<TR>'
        field_count += 1
    subgraph.add_subgraph(graph)
    return inner_table(body)

def add_to_graph_table(categorized, graph):
    print('add_to_graph_table')
    graph.node(categorized.get_node_name(),
               outer_table(make_body(categorized, graph, make_table_body)),
               xlabel=categorized.get_type_name())
