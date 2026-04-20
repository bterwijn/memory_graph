import string
import random

def create_graph(names, nr_edges):
    graph = {}
    names_set = set(names)
    for i in names:
        valid_edges = list(names_set - {i})
        graph[i] = ''.join([ e for e in random.sample(valid_edges, nr_edges)])
    return graph

def depth_first(graph, begin, end):
    
    def depth_first_recursive(graph, path, end, paths_all):
        """ 'path' is mutable to minimize copying """
        current = path[-1]
        if current == end:
            paths_all.append(path.copy())  # only copy completed path
        else:
            if current in graph:
                for n in graph[current]:
                    if n not in path:
                        path.append(n)  # do
                        depth_first_recursive(graph, path, end, paths_all)
                        path.pop()      # undo
        
    paths_all = []
    depth_first_recursive(graph, [begin], end, paths_all)
    return paths_all

nr_nodes = 26
nr_edges = 3
graph = create_graph(string.ascii_lowercase[:nr_nodes], nr_edges)
paths_all = depth_first(graph, 'a', 'b')
print(paths_all)
