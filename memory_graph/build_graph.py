import memory_graph.config_helpers as config_helpers

def add_subgraph(graphviz_graph, edges, subgraphed_nodes):
    """
    Helper function to add 'edges' to the graphviz graph. Each edges is a tuple (parent,child) where parent 
    and child are node names. Each edge is added to the graph only once.
    """
    new_edges = [child for _,child,_ in edges if child not in subgraphed_nodes]
    if len(new_edges) > 1:
        graphviz_graph.body.append('{ rank="same"  '+(" -> ".join(new_edges))+'  [weight=99,style=invis]; }\n')
    for c in new_edges:
        subgraphed_nodes.add(c)

def add_to_graphviz_graph(graphviz_graph, node, slices, sliced_elements, subgraphed_nodes, depth):
    #print('node:',node, 'data:',node.get_data(), 'slices:',slices)
    html_table = node.get_html_table(slices, sliced_elements)
    edges = html_table.get_edges()
    # ------------ subgraph
    add_subgraph(graphviz_graph, edges, subgraphed_nodes)
    # ------------ node
    color = config_helpers.get_color(node)
    border = 3 if node.is_root() else 1
    graphviz_graph.node(node.get_name(),
                        html_table.to_string(border, color),
                        xlabel=node.get_label(slices))
    # ------------ edges
    for parent,child,dashed in edges:
        graphviz_graph.edge(parent, child+':table', style='dashed' if dashed else 'solid')

def build_graph_depth_first(graphviz_graph, element, sliced_elements, visited_elements, subgraphed_nodes):
    if element in visited_elements:
        return
    visited_elements.add(element)
    children = element.get_children()
    slices = None
    if element in sliced_elements:
        slices = sliced_elements[element]
        if not slices is None:
            for index in slices:
                child = children[index]
                build_graph_depth_first(graphviz_graph, child, sliced_elements, visited_elements, subgraphed_nodes)
    if element.is_node() and not element.is_hidden_node() or element.is_root():
        add_to_graphviz_graph(graphviz_graph, element, slices, sliced_elements, subgraphed_nodes)

def build_graph_breadth_first(graphviz_graph, all_elements, sliced_elements, visited_elements, subgraphed_nodes, depth):
    new_children = []
    for element in all_elements:
        if not element in visited_elements:
            visited_elements.add(element)
            children = element.get_children()
            slices = None
            if element in sliced_elements:
                slices = sliced_elements[element]
                if not slices is None:
                    for index in slices:
                        child = children[index]
                        new_children.append(child)
    if len(new_children) > 0:
        build_graph_breadth_first(graphviz_graph, new_children, sliced_elements, visited_elements, subgraphed_nodes, depth+1)
    for element in all_elements:
        if element.is_node() and not element.is_hidden_node() or element.is_root():
            slices = None
            if element in sliced_elements:
                slices = sliced_elements[element]
            add_to_graphviz_graph(graphviz_graph, element, slices, sliced_elements, subgraphed_nodes, depth)

def build_graph(graphviz_graph, root_element, sliced_elements):
    #build_graph_depth_first(graphviz_graph, root_element, sliced_elements, set(), set())
    build_graph_breadth_first(graphviz_graph, [root_element], sliced_elements, set(), set(), 0)