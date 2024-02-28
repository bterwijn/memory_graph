import graphviz
new_graph=None
graph_attr={}
node_attr={'shape':'plaintext'}
edge_attr={}

import memory_visitor
visit_count = 0
id_to_name = {}
references = []

def give_name(data):
    global visit_count
    id_to_name[id(data)] = 'node'+str(visit_count)
    visit_count += 1

def get_name(data):
    return id_to_name[id(data)]

def visit_callback(data,parent):
    give_name(data)

def backtrack_callback(data,children):
    global new_graph
    print('backtrack data:',data,'name:',get_name(data),'children:',children)
    data_name = f'{get_name(data)}:X'
    named_children = [f'{get_name(c)}:X' for c in children]
    for index,child_name in enumerate(named_children):
        data_index_name = f'{get_name(data)}:{index}'
        references.append( (data_index_name, child_name))
    if len(named_children) > 1:
        lineup = " -> ".join(named_children)
        new_graph.body.append('{ rank="same"  '+lineup+'  [weight=99,style=invis]; }\n')
    new_graph.node(data_name, data_name, xlabel='xlabel')

memory_visitor.visit_callback = visit_callback
memory_visitor.visit_backtrack_callback = backtrack_callback

def print_nodes():
    for k,v in id_to_name.items():
        print('id:',k,'name:',v)

def print_references():
    for k,v in references:
        print('reference:',k,'->',v)

def graph(data):
    global visit_count, new_graph
    visit_count = 0
    id_to_name.clear()
    references.clear()
    new_graph=graphviz.Digraph('memory_graph',
                           graph_attr=graph_attr,
                           node_attr=node_attr,
                           edge_attr=edge_attr)
    memory_visitor.visit(data)
    print_nodes()
    print_references()
    return new_graph

if __name__ == '__main__':
    data = [[1,2], [3,4]]
    data.append(data[0])
    data.append(data)
    new_graph = graph(data)
    #new_graph.view()
    new_graph.render(outfile='what.gv')

