import string
import random
random.seed(0) # same random graph each run

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

def create_graph(names, nr_edges=2):
    # create nodes
    nodes = []
    for n in names:
        nodes.append(Node(n))
    # create edges
    for n in nodes:
        while True:
            n2 = random.choice(nodes)
            if n2 is not n and n2 not in n.get_edges():
                n.add_edge(n2)
                if len(n.get_edges()) >= nr_edges:
                    break     
    return nodes[0]

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

nr_nodes = 8
begin_node = create_graph(string.ascii_lowercase[:nr_nodes])
shortest_paths = breadth_first_paths(begin_node, 'b')
print(f'{shortest_paths=}')
