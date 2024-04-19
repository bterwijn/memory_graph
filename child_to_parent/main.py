
class Identities:

    def __init__(self):
        self.identities = {}
    
    def add(self, obj):
        identity = id(obj)
        if identity in self.identities:
            return (True, identity)
        self.identities[identity] = obj
        return (False, identity)
    
    def get(self, identity):
        return self.identities.get(identity)
    

class Graph:

    def __init__(self) -> None:
        self.parents = {}
        self.children = {}

    def __repr__(self) -> str:
        s = "Graph\n=== parents:\n"
        for parent_id,child_ids in self.parents.items():
            s += f"{parent_id} : {child_ids}\n"
        s += "=== children:\n"
        for child_id,parents_indices in self.children.items():
            s += f"{child_id} : {parents_indices}\n"
        return s

    def add(self, parent_id, child_ids):
        self.parents[parent_id] = child_ids
        for index, child in enumerate(child_ids):
            if not child in self.children:
                self.children[child]={}
            if not parent_id in self.children[child]:
                self.children[child][parent_id] = []
            self.children[child][parent_id].append(index)

    def get_children(self):
        return self.children
    
    def get_parents(self):
        return self.parents

    def get_children(self, parent):
        return self.parents[parent]
    
    def get_parents(self, child):
        return self.children[child]
    
class Sliced_Graph:

    def __init__(self, root_id, graph) -> None:
        self.graph = graph
        self.parents = {}
        self.slice(root_id)

    def __repr__(self) -> str:
        s = "Sliced_Graph\n=== parents:\n"
        for parent_id in self.parents:
            s += f"{parent_id} : {self.get_children(parent_id)}\n"
        return s

    def slice(self, data_id, n=3):
        if data_id in self.parents:
            return
        sliced_children = self.graph.get_children(data_id)
        if len(sliced_children) > n:
            sliced_children = sliced_children[:n]
            self.parents[data_id] = sliced_children
        else:
            self.parents[data_id] = None
        for child in sliced_children:
            self.slice(child)

    def get_parents(self):
        return self.parents
    
    def get_children(self, parent):
        sliced_children = self.parents[parent]
        if sliced_children is None:
            return self.graph.get_children(parent)
        return sliced_children

def visit_recursive(data, identities, graph):
    found, identity = identities.add(data)
    if not found:
        child_ids = []
        if isinstance(data, list):
            child_ids = [visit_recursive(child, identities, graph) for child in data]
        graph.add(identity, child_ids)
    return identity

def visit(data, identities, graph):
    return visit_recursive(data, identities, graph)

def main():
    child = ['c', 'h', 'i', 'l', 'd']
    long = [i for i in range(10)] + [child] + [i for i in range(10)]
    data =  [ long, child]
    print(data) 
    graph = Graph()
    identities = Identities()
    root_id = visit(data, identities, graph)
    print('root_id:', root_id)
    print(graph)
    sliced_graph = Sliced_Graph(root_id, graph)
    print(sliced_graph)

main()