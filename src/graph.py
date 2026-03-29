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

def print_path(path):
    for n in path:
        print(n.name, end=' ')
    print()

def print_paths(begin_node, end_name):
    def print_paths_recursive(end_name, path):
        cur = path[-1]
        if cur.name == end_name:
            print_path(path)
        else:
            neighbors = cur.get_edges()
            for n in neighbors:
                if not n in path:
                    path.append(n)
                    print_paths_recursive(end_name, path)
                    path.pop()
        
    path = [begin_node]
    print_paths_recursive(end_name, path)

nr_nodes = 8
graph = create_graph(string.ascii_lowercase[:nr_nodes])
print_paths(graph, 'b')

