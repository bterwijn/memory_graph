import string
import random

def create_graph(names, nr_edges):
    graph = {}
    names_set = set(names)
    for i in names:
        valid_edges = list(names_set - {i})
        graph[i] = ''.join([ e for e in random.sample(valid_edges, nr_edges)])
    return graph

def breadth_first(graph, begin, end):
    paths = [ begin ]
    paths_shortest = []
    while True:
        paths_new = []
        for path in paths:
            current = path[-1]
            if current == end:
                paths_shortest.append(path)
            else:
                if current in graph:
                    for n in graph[current]:
                        if n not in path:
                            paths_new.append(path + n)
        paths = paths_new
        if paths_shortest or not paths:
            return paths_shortest

nr_nodes = 26
nr_edges = 2
graph = create_graph(string.ascii_lowercase[:nr_nodes], nr_edges)
paths_shortest = breadth_first(graph, 'a', 'b')
print(paths_shortest)
