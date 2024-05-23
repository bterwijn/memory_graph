import memory_graph.config_helpers as config_helpers

def create_depth_for_nodes(elements_at_depth):
    depth_for_nodes = {}
    for element,depth in elements_at_depth.items():
        if element.is_node() and not element.is_hidden_node():
            if not depth in depth_for_nodes:
                depth_for_nodes[depth] = []
            depth_for_nodes[depth].append(element)
    return depth_for_nodes

def add_subgraph(graphviz_graph, nodes_to_subgraph):
    new_node_names = [node.get_name() for node in nodes_to_subgraph]
    if len(new_node_names) > 1:
        #graphviz_graph.body.append('{ rank="same"  '+(" -> ".join(new_node_names))+'  [weight=999,style=invis]; }\n')
        graphviz_graph.body.append('{ rank="same"  '+('; '.join(new_node_names))+'; }\n')

def add_to_graphviz_graph(graphviz_graph, node, slices, sliced_elements, subgraphed_nodes, depth):
    #print('node:',node, 'data:',node.get_data(), 'slices:',slices)
    html_table = node.get_html_table(slices, sliced_elements)
    edges = html_table.get_edges()
    color = config_helpers.get_color(node)
    border = 3 if node.is_root() else 1
    graphviz_graph.node(node.get_name(),
                        html_table.to_string(border, color),
                        xlabel=node.get_label(slices))
    # ------------ edges
    for parent,child,dashed in edges:
        graphviz_graph.edge(parent, child+':table', style='dashed' if dashed else 'solid')

def build_graph_depth_first(graphviz_graph, element, sliced_elements, elements_at_depth, subgraphed_nodes, depth):
    if element in elements_at_depth:
        return
    elements_at_depth[element] = depth
    children = element.get_children()
    slices = None
    if element in sliced_elements:
        slices = sliced_elements[element]
        if not slices is None:
            for index in slices:
                child = children[index]
                build_graph_depth_first(graphviz_graph, child, sliced_elements, elements_at_depth, subgraphed_nodes, depth+1)
    if element.is_node() and not element.is_hidden_node() or element.is_root():
        add_to_graphviz_graph(graphviz_graph, element, slices, sliced_elements, subgraphed_nodes, depth)

def build_graph(graphviz_graph, root_element, sliced_elements):
    elements_at_depth = {}
    build_graph_depth_first(graphviz_graph, root_element, sliced_elements, elements_at_depth, set(), 0)
    depth_for_nodes = create_depth_for_nodes(elements_at_depth)
    for depth, nodes in depth_for_nodes.items():
        add_subgraph(graphviz_graph, nodes)
        print('depth:',depth, 'nodes:',nodes)
