import copy
import bisect
import math

def my_round(value):
    """ Rounds the value to the nearest integer rounding '.5' up consistantly. """
    return math.floor(value + 0.5)

class ID_To_Data:

    def __init__(self):
        self.id_to_data = {}
    
    def add(self, obj):
        identity = id(obj)
        if identity in self.id_to_data:
            return (True, identity)
        self.id_to_data[identity] = obj
        return (False, identity)
    
    def __index__(self, identity):
        return self.id_to_data[identity]
    

class Full_Graph:

    def __init__(self, data, id_to_data) -> None:
        self.parents = {}
        self.children = {}
        root_id = self.build_graph_recursive(data, id_to_data)
        self.add_root(root_id)

    def __repr__(self) -> str:
        s = "Full_Graph\n=== parents:\n"
        for parent_id,child_ids in self.parents.items():
            s += f"{parent_id} : {child_ids}\n"
        s += "=== children:\n"
        for child_id,parents_indices in self.children.items():
            s += f"{child_id} : {parents_indices}\n"
        return s

    def build_graph_recursive(self, data, id_to_data):
        found, identity = id_to_data.add(data)
        if not found:
            child_ids = []
            if isinstance(data, list):
                child_ids = [self.build_graph_recursive(child, id_to_data) for child in data]
            self.add(identity, child_ids)
        return identity

    def add(self, parent_id, child_ids):
        self.parents[parent_id] = child_ids
        for index, child in enumerate(child_ids):
            if not child in self.children:
                self.children[child]={}
            if not parent_id in self.children[child]:
                self.children[child][parent_id] = []
            self.children[child][parent_id].append(index)

    def add_root(self, parent_id):
        self.children[parent_id] = {}
        self.root = parent_id

    def get_root(self):
        return self.root

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

    def add_slice(self, begin_end, remove_interposed_dots=1):
        insert0 = bisect.bisect_right(self.slices, begin_end[0], key=lambda x: x[0])
        insert1 = bisect.bisect_left (self.slices, begin_end[1], key=lambda x: x[1])
        merge_begin, merge_end = False, False
        if insert0 > 0:
            if self.slices[insert0-1][1] >= (begin_end[0] - remove_interposed_dots):
                merge_begin = True
        if insert1 < len(self.slices):
            if self.slices[insert1][0] <= (begin_end[1] + remove_interposed_dots):
                merge_end = True
        if merge_begin and merge_end:
            if insert0 - insert1 == 1: # no slices changed
                return False
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
        return True

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

    slices = test.copy()
    assert not slices.add_slice([10,11])
    assert not slices.add_slice([19,20])
    assert not slices.add_slice([30,31])
    assert not slices.add_slice([39,40])
    assert not slices.add_slice([65,66])
    assert slices.add_slice([9,10])
    assert slices.add_slice([20,21])
    assert slices.add_slice([28,29])
    assert slices.add_slice([41,42])
    assert slices.add_slice([75,76])
    assert slices.add_slice([100,200])

class Slicer:

    def __init__(self, begin=None, end=None, middle=None, /) -> None:
        self.begin = begin
        self.end = end
        self.middle = middle
        if not self.middle is None:
            self.end, self.middle = self.middle, self.end

    def __repr__(self) -> str:
        return f"Slicer({self.begin},{self.middle},{self.end})"

    def get_slices(self, length):
        slices = Slices()
        if self.begin is None:
            slices.add_slice([0, length])
        else:
            if isinstance(self.begin, float):
                slices.add_slice([0, 
                                  min(length,my_round(length*self.begin))]) # TODO: my_round
            else:
                slices.add_slice([0, 
                                  min(length,self.begin)])
            if not self.middle is None:
                mid = length/2
                if isinstance(self.middle, float):
                    half = length*self.middle/2
                else:
                    half = self.middle/2
                slices.add_slice([max(0,my_round(mid-half)), 
                                  min(length,my_round(mid+half))])
            if not self.end is None:
                if isinstance(self.end, float):
                    slices.add_slice([max(0,my_round(length-length*self.end)),
                                      length])
                else:
                    slices.add_slice([max(0,length-self.end),
                                      length])
        #print("slices:",slices)
        return slices

def test_slicer():
    slicer = Slicer(0.1, 0.2, 0.3)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [40, 60], [70, 100]], "Slicer error"

    slicer = Slicer(10, 20, 30)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [40, 60], [70, 100]], "Slicer error"

    slicer = Slicer(0.1, 0.3)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [70, 100]], "Slicer error"

    slicer = Slicer(10, 30)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [70, 100]], "Slicer error"

    slicer = Slicer(0.1)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10]], "Slicer error"

    slicer = Slicer(10)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10]], "Slicer error"

    slicer = Slicer()
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 100]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(0)
    assert slices.get_slices() == [[0,0]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(5)
    assert slices.get_slices() == [[0,5]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(6)
    assert slices.get_slices() == [[0,2],[4,6]], "Slicer error"

class Sliced_Graph:

    def __init__(self, full_graph, slicer) -> None:
        self.full_graph = full_graph
        self.slicer = slicer
        self.parents = {}
        self.slice(full_graph.get_root())

    def __repr__(self) -> str:
        s = "Sliced_Graph\n=== parents:\n"
        for parent_id in self.parents:
            s += f"{parent_id} : {self.get_slices(parent_id)} {self.full_graph.get_children(parent_id)}\n"
        return s

    def slice(self, data_id, n=3):
        if data_id in self.parents:
            return
        children = self.full_graph.get_children(data_id)
        print("children:",children, "slicer:", self.slicer)
        slices = self.slicer.get_slices(len(children))
        print("slices:",slices)
        self.parents[data_id] = slices
        for slice in slices.get_slices():
            for child in children[slice[0]:slice[1]]:
                self.slice(child)

    def get_parents(self):
        return self.parents
    
    def get_slices(self, parent):
        return self.parents[parent]
    
    def add_missing_edges(self):
        for p in self.get_parents():
            print("p:", p)
            self.add_paths_to_root(p)

    def add_paths_to_root(self, node):
        print('  node:',node)
        parents_indices = self.full_graph.get_parents(node)
        for parent, indices in parents_indices.items():
            all_new_edges = True
            for index in indices:
                print('    parent:',parent,'index:',index)
                slices = self.get_slices(parent)
                all_new_edges &= slices.add_slice([index,index+1], 0) 
            if all_new_edges:
                self.add_paths_to_root(parent)

def main():
    child = [i*100 for i in range(1,10)]
    long = [i for i in range(10)]
    long.insert(4, child)
    long.insert(6, child)
    data =  [ long, child]
    print(data)

    id_to_data = ID_To_Data()
    full_graph = Full_Graph(data, id_to_data)
    print(full_graph)

    test_slices()
    test_slicer()

    sliced_graph = Sliced_Graph(full_graph, Slicer(2,2))
    print(sliced_graph)
    sliced_graph.add_missing_edges()
    print(sliced_graph)

main()