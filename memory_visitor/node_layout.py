import memory_visitor
import categories
import node_builder
import utils
import types
import html
import children

drop_child_references_types = {}#utils.class_type, dict, }

orientation_linear    = None # 'v' (vertical), 'h' (horizontal), None (based on ref_count)
orientation_key_value = None # 'v' (vertical), 'h' (horizontal), None (based on ref_count)

max_string_length = 42

type_to_color = {
    # ================= singular
    type(None) : "gray",
    bool : "pink",
    int : "green",
    float : "violetred1",
    complex : "yellow",
    str : "cyan",
    # ================= linear
    tuple : "orange",
    list : "lightcoral",
    set : "orchid1",
    frozenset : "orchid2",
    bytes : "khaki1",
    bytearray : "khaki2",
    # ================= key_value
    dict : "dodgerblue1",
    types.MappingProxyType : "red", #"dodgerblue2", # not used
    utils.class_type : "seagreen1",
    type: "seagreen2", # where class variable are stored
}
default_color_singular = "white"
default_color_linear = "white"
default_color_key_value = "white"
default_color_table = "bisque2"


def drop_child_references_of_types(type1, type2):
    return type1 in drop_child_references_types or type2 in drop_child_references_types

def drop_child_references(categorized):
    return drop_child_references_of_types(type(categorized.get_data()), 
                                          categorized.get_alternative_type())

def is_vertical(orientation, ref_count):
    if orientation == 'h':
        return False
    if orientation == 'v':
        return True
    return ref_count == 0

def format_string(data):
    s = str(data)
    s = (s[:max_string_length] + '..') if len(s) > max_string_length else s
    return html.escape(s)

def get_color(categorized, default_color='white'):
    datatype = type(categorized.get_data())
    if datatype in type_to_color:
        return type_to_color[datatype]
    alternative_type = categorized.get_alternative_type()
    if alternative_type in type_to_color:
        return type_to_color[alternative_type]
    return default_color

def outer_table(categorized, s, color='white'):
    color = get_color(categorized, color)
    border = 1 if categorized.get_parent() else 3
    return (f'<\n<TABLE BORDER="0" CELLBORDER="{border}" CELLSPACING="0" CELLPADDING="0" BGCOLOR="{color}"><TR><TD PORT="X">\n' +
            s + '\n</TD></TR></TABLE>\n>')

def inner_table(s):
    return ('<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="5" CELLPADDING="0"><TR>\n' +
            s + '\n</TR></TABLE>')

def table_entry_ref(field):
    return f'<TD PORT="{field}"> </TD>'

def table_entry_ref_rounded(field):
    return f'<TD PORT="{field}" STYLE="ROUNDED"> </TD>'

def table_entry_str(s):
    return f'<TD> {format_string(s)} </TD>'

def table_entry_str_rounded(s):
    return f'<TD STYLE="ROUNDED"> {format_string(s)} </TD>'

def table_empty():
    return '<TD> </TD>'

def table_new_line():
    return '</TR>\n<TR>'

def table_dots():
    return '<TD>...</TD>'

def get_xlabel_1d(categorized):
    return f'{categorized.get_type_name()} ({len(categorized.get_children())})'

def get_xlabel_2d(categorized):
    x,y = categorized.get_size()
    return f'{categorized.get_type_name()} ({x}x{y})'

def make_body(categorized, graph, fun):
    if len(categorized.get_children()) == 0:
        return f' {format_string(categorized.get_data())} '
    return fun(categorized, graph)

def add_to_graph_singular(categorized, graph):
    graph.node(categorized.get_node_name(),
                outer_table(categorized, str(categorized.get_data()), default_color_singular),
                xlabel=categorized.get_type_name())

def make_linear_body(categorized, graph):
    nbuilder = node_builder.Node_Builder(graph)
    #categorized.get_children().map(lambda child : print('lin child:',child) )
    entries = categorized.get_children().map(lambda child : 
                                             nbuilder.make_table_entry(categorized, child, table_entry_str, table_entry_ref)
                                             )
    nbuilder.write_subgraph()
    #print('entries:',entries.get_children())
    body0 = ''
    for level,child in children.Child_Iterator_Linear(entries.get_children()):
        #print("level:", level, "child:", child)
        if abs(level) == 1: # or level < -1:
            body0 += table_dots()
        if child:
            body0 += child
    #print("body0:", body0)
    return inner_table(body0)

def add_to_graph_linear(categorized, graph):
    parent = categorized.get_parent()
    if parent and drop_child_references(parent):
        return
    graph.node(categorized.get_node_name(),
               outer_table(categorized, make_body(categorized, graph, make_linear_body), default_color_linear),
               xlabel=get_xlabel_1d(categorized))

def make_key_value_body(categorized, graph):
    nbuilder = node_builder.Node_Builder(graph)
    #entries = categorized.get_children().map(lambda child : print('key child:',child) )
    entries = categorized.get_children().map(lambda child : 
                                             nbuilder.make_table_entry(categorized, child, table_entry_str, table_entry_ref)
                                             )
    entries = entries.get_children()
    nbuilder.write_subgraph()
    vertical = is_vertical(orientation_linear, nbuilder.get_ref_count())
    body = entries[0] if len(entries[0]) > 0 else [table_empty()]
    if len(entries[1]) > 0:
        body += [table_dots()] + entries[1]
    if vertical:
        body = table_new_line().join(body)
    else:
        body = ''.join(body)
    return inner_table(body)

    vertical = is_vertical(orientation_key_value, nbuilder.get_ref_count())
    body = entries[0]
    if len(entries[1]) > 0:
        body += [table_dots()] + entries[1]
    if vertical:
        body = table_new_line().join(body)
    else:
        body = ''.join(body)
    # if vertical:
    #     body = table_new_line().join([ entries_key[i] + entries_value[i] for i in range(len(entries_key))]) 
    # else:
    #     body = ''.join(entries_key) + table_new_line() + ''.join(entries_value)
    return inner_table(body)

def add_to_graph_key_value(categorized, graph):
    if drop_child_references(categorized):
        graph.node(categorized.get_node_name(),
                   outer_table(categorized, make_body(categorized, graph, make_key_value_body), default_color_key_value),
                   xlabel=get_xlabel_1d(categorized))
    else:
        graph.node(categorized.get_node_name(),
                   outer_table(categorized, make_body(categorized, graph, make_linear_body), default_color_key_value),
                   xlabel=get_xlabel_1d(categorized))


def make_table_body(categorized, graph):
    nbuilder = node_builder.Node_Builder(graph)
    #entries = categorized.get_children().map(lambda child : print('table child:',child) )

    print('table children:',categorized.get_children())
    entries = categorized.get_children().map(lambda child : 
                                             nbuilder.make_table_entry(categorized, child, table_entry_str, table_entry_ref)
                                             )
    nbuilder.write_subgraph()
    print('entries children:',entries.get_children())

    #row_names = children.front_back_split(categorized.get_row_names(),categorized.max_height)
    #print("row_names:", row_names)
    #column_names = children.front_back_split(categorized.get_column_names(), categorized.max_width)
    #print("column_names:", column_names)

    body = ''
    first_line = True
    add_new_line = False
    for level,child in children.Child_Iterator_Table(entries.get_children()):
        print("level:", level, "child:", child)
        if add_new_line:
            body += table_new_line()
            add_new_line = False
        if abs(level) == 1:
            body += table_dots()
            first_line = False
        if abs(level) == 2:
            body += table_new_line()
        elif abs(level) == 3:
            if not first_line:
                body += table_new_line()
            body += table_dots()
            if level<0:
                add_new_line = True
            else:
                body += table_new_line()
        if child:
            body += child
            first_line = False
    print("body:\n", body)
    return inner_table(body)

def add_to_graph_table(categorized, graph):
    graph.node(categorized.get_node_name(),
               outer_table(categorized, make_body(categorized, graph, make_table_body), default_color_table),
               xlabel=get_xlabel_2d(categorized))
