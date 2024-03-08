import memory_visitor
import categories
import utils
import types

drop_child_references_types = {utils.class_type, dict, }
no_drop_child_references_types = set()

linear_orientation = 'h'
key_value_orientation = 'h'

type_to_color = {
    # ================= singular
    type(None) : "gray",
    bool : "pink",
    int : "green",
    float : "mediumorchid1",
    complex : "yellow",
    str : "cyan",
    # ================= linear
    tuple : "orange",
    list : "lightcoral",
    set : "darkolivegreen1",
    frozenset : "darkolivegreen2",
    bytes : "cyan",
    bytearray : "cyan",
    # ================= key_value
    dict : "royalblue1",
    types.MappingProxyType : "royalblue2",
    utils.class_type : "seagreen1",
    type: "seagreen2", # where class variable are stored
}
default_color_singular = "white"
default_color_linear = "white"
default_color_key_value = "white"
default_color_table = "bisque2"


def drop_child_references(categorized):
    type1 = type(categorized.get_data())
    type2 = categorized.get_alternative_type()
    return ((type1 in drop_child_references_types or type2 in drop_child_references_types) and not
            (type1 in no_drop_child_references_types or type2 in no_drop_child_references_types))

def get_color(categorized, default_color='white'):
    datatype = type(categorized.get_data())
    if datatype in type_to_color:
        return type_to_color[datatype]
    alternative_type = categorized.get_alternative_type()
    if alternative_type in type_to_color:
        return type_to_color[alternative_type]
    return default_color

def outer_table(s, color='white'):
    return (f'<\n<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X">\n' +
            s + '\n</TD></TR></TABLE>\n>')

def inner_table(s):
    return ('<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5" CELLPADDING="0"><TR>\n' +
            s + '\n</TR></TABLE>')

def table_entry_ref(field):
    return f'<TD PORT="{field}"> </TD>'

def table_entry_ref_rounded(field):
    return f'<TD PORT="{field}" STYLE="ROUNDED"> </TD>'

def table_entry_str(s):
    return f'<TD> {utils.to_string(s)} </TD>'

def table_entry_str_rounded(s):
    return f'<TD STYLE="ROUNDED"> {utils.to_string(s)} </TD>'

def table_new_line():
    return '</TR>\n<TR>'

def get_xlabel_1d(categorized):
    return f'{categorized.get_type_name()} ({len(categorized.get_children())})'

def get_xlabel_2d(categorized):
    x,y = categorized.get_size()
    return f'{categorized.get_type_name()} ({x}x{y})'

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
                   outer_table(str(categorized.get_data()),get_color(categorized, default_color_singular)),
                   xlabel=categorized.get_type_name())

def make_table_entry(categorized, child, graph, subgraph, entry_count, ref_count, fun_str, fun_ref):
    if type(child) == str:
        entry = fun_str(child)
    else:
        field = f'f{entry_count}'
        entry = fun_ref(field)
        cname = f'{child.get_node_name()}:X'
        graph.edge(f'{categorized.get_node_name()}:{field}', cname)
        subgraph.add_child(child)
        ref_count += 1
    return entry_count+1, ref_count, entry

def make_body(categorized, graph, fun):
    if len(categorized.get_children()) == 0:
        return f' {utils.to_string(categorized.get_data())} '
    return fun(categorized, graph)

def make_linear_body(categorized, graph):
    entries = []
    entry_count = 0
    ref_count = 0
    subgraph = Subgraph()
    for child in categorized.get_children():
        entry_count, ref_count, entry = make_table_entry(categorized, child, graph, subgraph, entry_count, ref_count,
                                                        table_entry_str, table_entry_ref)
        entries.append(entry)
    subgraph.add_subgraph(graph)
    vertical = (ref_count == 0)
    if vertical:
        body = table_new_line().join(entries)
    else:
        body = ''.join(entries)
    return inner_table(body)

def add_to_graph_linear(categorized, graph):
    parent = categorized.get_parent()
    if parent and drop_child_references(parent):
        return
    graph.node(categorized.get_node_name(),
               outer_table(make_body(categorized, graph, make_linear_body), get_color(categorized, default_color_linear)),
               xlabel=get_xlabel_1d(categorized))

def make_key_value_body(categorized, graph):
    entries_key = []
    entries_value = []
    entry_count = 0
    ref_count = 0
    subgraph = Subgraph()
    for child in categorized.get_children():
        entry_count, ref_count, entry = make_table_entry(categorized, child.get_children()[0], graph, subgraph, entry_count, ref_count,
                                                        table_entry_str_rounded, table_entry_ref_rounded)
        entries_key.append(entry)
        entry_count, ref_count, entry = make_table_entry(categorized, child.get_children()[1], graph, subgraph, entry_count, ref_count,
                                                        table_entry_str, table_entry_ref)
        entries_value.append(entry)
    subgraph.add_subgraph(graph)
    vertical = (ref_count == 0)
    if vertical:
        body = table_new_line().join([ entries_key[i] + entries_value[i] for i in range(len(entries_key))]) 
    else:
        body = ''.join(entries_key) + table_new_line() + ''.join(entries_value)
    return inner_table(body)

def add_to_graph_key_value(categorized, graph):
    if drop_child_references(categorized):
        graph.node(categorized.get_node_name(),
                   outer_table(make_body(categorized, graph, make_key_value_body), get_color(categorized, default_color_key_value)),
                   xlabel=get_xlabel_1d(categorized))
    else:
        graph.node(categorized.get_node_name(),
                   outer_table(make_body(categorized, graph, make_linear_body), get_color(categorized, default_color_key_value)),
                   xlabel=get_xlabel_1d(categorized))

def make_table_body(categorized, graph):
    entries = []
    entry_count = 0
    ref_count = 0
    row_names = categorized.get_row_names()
    column_names = categorized.get_column_names()
    entries_row_names = [table_entry_str_rounded(n) for n in row_names]
    entries_column_names = [table_entry_str_rounded('')] if row_names and column_names else []
    entries_column_names += [table_entry_str_rounded(n) for n in column_names]
    subgraph = Subgraph()
    for child in categorized.get_children():
        entry_count, ref_count, entry = make_table_entry(categorized, child, graph, subgraph, entry_count, ref_count,
                                                        table_entry_str, table_entry_ref)
        entries.append(entry)
    subgraph.add_subgraph(graph)
    body = ''
    if entries_column_names:
       body += ''.join(entries_column_names) + table_new_line()
    nr_columns = categorized.get_size()[1]
    row_count = 0
    for i in range(0,len(entries),nr_columns):
        if row_count > 0:
            body += table_new_line()
        if row_count<len(entries_row_names):
            body += entries_row_names[row_count]
        row_count += 1
        body += ''.join(entries[i:i+nr_columns])
    return inner_table(body)

def add_to_graph_table(categorized, graph):
    graph.node(categorized.get_node_name(),
               outer_table(make_body(categorized, graph, make_table_body), get_color(categorized, default_color_table)),
               xlabel=get_xlabel_2d(categorized))
