from memory_graph.node           import Node
from memory_graph.node_key_value import Node_Key_Value
import memory_graph.node
from memory_graph.slices import Slices1D

def is_tuple_with_key_value_parent(node, graph_full) -> bool:
    if node.get_type() is tuple:
        parents_indices = graph_full.get_parents(node.get_id())
        if len(parents_indices) == 1 and type(graph_full.get_node(next(iter(parents_indices)))) is Node_Key_Value:
            return True
    return False

class Graph_Sliced:

    def __init__(self, graph_full, depth) -> None:
        self.graph_full = graph_full
        self.id_to_slices = {}
        self.slice(graph_full.get_root_id(), depth)

    def get_graph_full(self):
        return self.graph_full

    def __repr__(self) -> str:
        s = "Graph_Sliced\n=== parents:\n"
        for node_id in self.id_to_slices:
            s += f"{node_id} : {self.get_slices(node_id)} {self.graph_full.get_node(node_id)}\n"
        return s

    def slice(self, node_id, depth):
        if depth == 0 or node_id in self.id_to_slices:
            return
        node = self.graph_full.get_node(node_id)
        if memory_graph.node.is_separate_node(node):
            children = node.get_children()
            if not children is None:
                slicer = node.get_slicer()
                slices = children.slice(slicer)
                #print('node:',node,'slicer:',slicer, 'slices:',slices)
                self.id_to_slices[node_id] = slices
                if not is_tuple_with_key_value_parent(node, self.graph_full):
                    depth -= 1
                for index in slices:
                    self.slice(id(children[index]), depth)
            else:
                self.id_to_slices[node_id] = None # for nodes without children

    def get_node_ids(self):
        return self.id_to_slices
    
    def get_slices(self, node_id):
        return self.id_to_slices[node_id]
    
    def has_slices(self, node_id):
        return node_id in self.id_to_slices
    
    def add_missing_edges(self):
        for node_id in list(self.get_node_ids().keys()):
            print("node_id:", node_id)
            self.add_paths_to_root(node_id)

    def add_paths_to_root(self, node_id):
        print('  node_id:',node_id)
        parents_indices = self.graph_full.get_parents(node_id)
        for parent_id, indices in parents_indices.items():
            new_parent = False
            if not parent_id in self.id_to_slices:
                new_parent = True
                parent = self.graph_full.get_node(parent_id)
                slices = parent.get_children().empty_slice()
                self.id_to_slices[parent_id] = slices
            else:
                slices = self.get_slices(parent_id)
            for index in indices:
                print('    parent_id:',parent_id,'index:',index)
                slices.add_index(index)
            if new_parent:
                self.add_paths_to_root(parent_id)

    def process_nodes(self, callback):
        if self.graph_full.size() == 1:
            node = self.graph_full.get_node(self.graph_full.get_root_id())
            if not isinstance(node, Node):
                node = Node(node)
            callback(node, Slices1D([[0,1]]), self)
        else:
            self.process_nodes_recursive(self.graph_full.get_root_id(), callback, set())

    def process_nodes_recursive(self, node_id, callback, id_to_count):
        if not node_id in id_to_count:
            id_to_count.add(node_id)
            node = self.graph_full.get_node(node_id)
            if memory_graph.node.is_separate_node(node) and self.has_slices(node_id):
                slices = self.get_slices(node_id)
                children = node.get_children()
                if not children is None:
                    for index in slices:
                        child_id = id(children[index])
                        self.process_nodes_recursive(child_id, callback, id_to_count)
                callback(node, slices, self)
