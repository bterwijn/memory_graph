import copy
import bisect

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

class Slices:

    def __init__(self, slices=None) -> None:
        self.slices = []
        if not slices is None:
            for i in slices:
                self.add_slice(i)

    def __repr__(self) -> str:
        return f"Slices({self.slices})"
    
    def copy(self):
        s = Slices()
        s.slices = copy.deepcopy(self.slices)
        return s

    def get_slices(self):
        return self.slices

    def add_slice(self, begin_end):
        insert0 = bisect.bisect_right(self.slices, begin_end[0], key=lambda x: x[0])
        insert1 = bisect.bisect_left (self.slices, begin_end[1], key=lambda x: x[1])
        merge_begin, merge_end = False, False
        if insert0 > 0:
            if self.slices[insert0-1][1] >= begin_end[0]-1:
                merge_begin = True
        if insert1 < len(self.slices):
            if self.slices[insert1][0] <= begin_end[1]+1:
                merge_end = True
        if merge_begin and merge_end:
            self.slices[insert0-1][1] = self.slices[insert1][1]
            del self.slices[insert0:insert1+1]
        elif merge_begin:
            self.slices[insert0-1][1] = max(self.slices[insert1-1][1], begin_end[1])
            del self.slices[insert0:insert1]
        elif merge_end:
            self.slices[insert1][0] = min(self.slices[insert0][0], begin_end[0])
            del self.slices[insert0:insert1]
        else:
            del self.slices[insert0:insert1]
            self.slices.insert(insert0, begin_end)

def test_slices():
    test = Slices( [[10,20], [30,40], [60,70], [80,90]] )
    slices = test.copy()
    slices.add_slice([21,79])
    assert slices.get_slices() == [[10,90]], "Slice error: merging begin and end"

    slices = test.copy()
    slices.add_slice([31,39])
    assert slices.get_slices() == [[10,20], [30,40], [60,70], [80,90]], "Slice error: merging begin and end"

    slices = test.copy()
    slices.add_slice([15,50])
    assert slices.get_slices() == [[10,50], [60,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([15,65])
    assert slices.get_slices() == [[10,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([35,45])
    assert slices.get_slices() == [[10,20], [30,45], [60,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([25,65])
    assert slices.get_slices() == [[10,20], [25,70], [80,90]], "Slice error: merging end"
    
    slices = test.copy()
    slices.add_slice([15,65])
    assert slices.get_slices() == [[10,70], [80,90]], "Slice error: merging end"

    slices = test.copy()
    slices.add_slice([55,65])
    assert slices.get_slices() == [[10,20], [30,40], [55,70], [80,90]], "Slice error: merging end"

    slices = test.copy()
    slices.add_slice([25,75])
    assert slices.get_slices() == [[10,20], [25,75], [80,90]], "Slice error: merging none"

    slices = test.copy()
    slices.add_slice([5,6])
    assert slices.get_slices() == [[5,6], [10,20], [30,40], [60,70], [80,90]], "Slice error: merging none"

    slices = test.copy()
    slices.add_slice([95,96])
    assert slices.get_slices() == [[10,20], [30,40], [60,70], [80,90], [95,96]], "Slice error: merging none"

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
    test_slices()

main()