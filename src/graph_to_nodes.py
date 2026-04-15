import string
import random

def create_graph(names, nr_edges):
    graph = {}
    names_set = set(names)
    for i in names:
        valid_edges = list(names_set - {i})
        graph[i] = ''.join([ e for e in random.sample(valid_edges, nr_edges)])
    return graph

class Node:
    
    def __init__(self, name):
        self.name = name
        self.edges = []
        
    def __repr__(self):
        return self.name + str([e.name for e in self.edges])
        
    def add_edge(self, node):
        self.edges.append(node)
        
    def get_edges(self):
        return self.edges

# configure memory_graph to show graph nicely
def node_table(d):
    if hasattr(d, 'edges'):
        cells = [[i] for i in [d.name] + d.edges]
        return mg.Node_Table(d, cells)
    else:
        return mg.Node_Table(d, [])
mg.config.type_to_node[Node] = node_table
mg.config.type_to_color[Node] = "aqua"

def graph_to_nodes(graph):
    # create nodes
    nodes = {}
    for n in graph:
        nodes[n]=Node(n)
    # create edges
    for n, edges in graph.items():
        for e in edges:
            nodes[n].add_edge(nodes[e])
    n, node = next(iter(nodes.items()))
    return node

def breadth_first_paths(begin_node, end_name):
    paths = [[begin_node]]
    shortest_paths = []
    while True:
        new_paths = []    
        for path in paths:
            current_node = path[-1]
            path[-1] = current_node.name
            if current_node.name == end_name:
                shortest_paths.append(path)
            else:
                if nodes := current_node.get_edges():
                    for node in nodes:
                        if node.name not in path:
                            pc = path.copy()
                            pc.append(node)
                            new_paths.append(pc)
        paths = new_paths
        if shortest_paths or not paths:
            break
    return shortest_paths

nr_nodes = 26
nr_edges = 2
graph = create_graph(string.ascii_lowercase[:nr_nodes], nr_edges)
begin_node = graph_to_nodes(graph)
shortest_paths = breadth_first_paths(begin_node, 'b')
print(shortest_paths)
