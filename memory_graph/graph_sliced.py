from memory_graph.element_base           import Element_Base
from memory_graph.element_key_value import Element_Key_Value
import memory_graph.element_base
from memory_graph.slices import Slices1D

# def is_tuple_with_key_value_parent(node, graph_full) -> bool:
#     #return False
#     if node.get_type() is tuple:
#         parents_indices = graph_full.get_parents(node.get_id())
#         if len(parents_indices) == 1 and type(graph_full.get_node(next(iter(parents_indices)))) is Element_Key_Value:
#             return True
#     return False

class Missing_Edges:

    def __init__(self):
        self.type_to_parents_indices = {}
        self.index_count = 0

    def __repr__(self) -> str:
        s = ""
        for type, parents_indices in self.type_to_parents_indices.items():
            s += f"{type} : {parents_indices}\n"
        return s

    def add_parent_index(self, type, parent_id, index):
        if not type in self.type_to_parents_indices:
            self.type_to_parents_indices[type] = {}
        if not parent_id in self.type_to_parents_indices[type]:
            self.type_to_parents_indices[type][parent_id] = []
        self.type_to_parents_indices[type][parent_id].append(index)
        self.index_count += 1

    def get_index_count(self):
        return self.index_count

class Graph_Sliced:

    def __init__(self, graph_full, depth=-1) -> None:
        self.graph_full = graph_full
        self.id_to_slices = {}
        self.node_ids = set()
        self.slice_graph(graph_full.get_root_id(), depth)

    def get_graph_full(self):
        return self.graph_full

    def __repr__(self) -> str:
        s = "Graph_Sliced\n=== parents:\n"
        for element_id in self.id_to_slices:
            s += f"{element_id}: {self.get_slices(element_id)} {self.graph_full.get_element_by_id(element_id)}\n"
        s+= f'node_ids: {self.node_ids}\n'
        return s

    def slice_graph(self, element_id, depth):
        if depth == 0 or element_id in self.id_to_slices:
            return
        element = self.graph_full.get_element_by_id(element_id)
        is_node = self.graph_full.is_node(element)
        if is_node:
            self.node_ids.add(element_id)
        children = self.graph_full.get_children(element)
        if not children is None:
            slicer = element.get_slicer()
            slices = children.slice(slicer)
            #print('element:',element,'slicer:',slicer, 'slices:',slices)
            self.id_to_slices[element_id] = slices
            if is_node:
                depth -= 1
            for index in slices:
                self.slice_graph(id(children[index]), depth)

    def get_element_ids(self):
        return self.id_to_slices
    
    def get_slices(self, element_id):
        return self.id_to_slices[element_id]
    
    def has_slices(self, element_id):
        return element_id in self.id_to_slices
    
    def get_node_ids(self):
        return self.node_ids
    
    def add_missing_edges(self):
        for element_id in self.node_ids.copy():
            print('add_missing_edges element_id:', element_id)
            self.add_missing_edges_recursive(element_id)

    def add_missing_edges_recursive(self, element_id):
        print("element_id:", element_id)
        missing_edges = self.find_missing_edges(element_id)
        print("missing_edges:", missing_edges)
        self.add_edges(missing_edges)

    def find_missing_edges(self, element_id):
        missing_edges = Missing_Edges()
        parents_indices = self.graph_full.get_parent_indices_by_id(element_id)
        for parent_id, indices in parents_indices.items():
            parent = self.graph_full.get_element_by_id(parent_id)
            type = parent.get_type()
            for index in indices:
                if parent_id in self.id_to_slices:
                    slices = self.get_slices(parent_id)
                    if not slices.has_index(index):
                        missing_edges.add_parent_index(type, parent_id, index)
                else:
                    missing_edges.add_parent_index(type, parent_id, index)
        return missing_edges
    
    def add_edges(self, missing_edges):
        for type, parents_indices in missing_edges.type_to_parents_indices.items():
            print('add_edges  type:',type)
            config_count = 3
            count = config_count
            for parent_id, indices in parents_indices.items():
                if count == 0:
                    break
                new_parent = False
                if not parent_id in self.id_to_slices:
                    new_parent = True
                    parent = self.graph_full.get_element_by_id(parent_id)
                    slices = parent.get_children().empty_slice()
                    self.id_to_slices[parent_id] = slices
                    if self.graph_full.is_node(parent):
                        self.node_ids.add(parent_id)
                else:
                    slices = self.get_slices(parent_id)
                for index in indices:
                    print('    parent_id:',parent_id,'index:',index)
                    is_dashed = config_count<missing_edges.get_index_count()
                    slices.add_index(index, dashed=is_dashed)
                    count -= 1
                if new_parent:
                    self.add_missing_edges_recursive(parent_id)

    def visit_all_nodes(self, callback):
        if self.graph_full.size() == 1:
            element = self.graph_full.get_element_by_id(self.graph_full.get_root_id())
            if not isinstance(element, Element_Base):
                element = Element_Base(element)
            callback(element, Slices1D([[0,1]]), self)
        else:
            self.visit_all_nodes_recursive(self.graph_full.get_root_id(), callback, set())

    def visit_all_nodes_recursive(self, element_id, callback, just_once):
        if not element_id in just_once:
            just_once.add(element_id)
            element = self.graph_full.get_element_by_id(element_id)
            slices = None
            if self.has_slices(element_id):
                slices = self.get_slices(element_id)
                children = element.get_children()
                for index in slices:
                    child_id = id(children[index])
                    self.visit_all_nodes_recursive(child_id, callback, just_once)
            print('element:',element)
            if element_id in self.node_ids:
                callback(element, slices, self)
