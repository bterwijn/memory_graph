from memory_graph.node import Node

class Graph_Sliced:

    def __init__(self, graph_full) -> None:
        self.graph_full = graph_full
        self.id_to_slices = {}
        self.slice(graph_full.get_root_id())

    def __repr__(self) -> str:
        s = "Graph_Sliced\n=== parents:\n"
        for node_id in self.id_to_slices:
            s += f"{node_id} : {self.get_slices(node_id)} {self.graph_full.get_node(node_id)}\n"
        return s

    def slice(self, node_id):
        if node_id in self.id_to_slices:
            return
        node = self.graph_full.get_node(node_id)
        if isinstance(node, Node):
            children = node.get_children()
            if not children is None:
                slicer = node.get_slicer()
                print('node:',node,'slicer:',slicer)
                slices = children.slice(slicer)
                self.id_to_slices[node_id] = slices
                for index in slices:
                    self.slice(id(children[index]))

    def get_node_ids(self):
        return self.id_to_slices
    
    def get_slices(self, node_id):
        return self.id_to_slices[node_id]
    
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
        self.process_nodes_recursive(self.graph_full.get_root_id(), callback, set())

    def process_nodes_recursive(self, node_id, callback, id_to_count):
        if not node_id in id_to_count:
            id_to_count.add(node_id)
            node = self.graph_full.get_node(node_id)
            if isinstance(node, Node):
                children = node.get_children()
                slices = None
                if not children is None:
                    slices = self.get_slices(node_id)
                    for index in slices:
                        child_id = id(children[index])
                        self.process_nodes_recursive(child_id, callback, id_to_count)
                callback(node, slices, self.graph_full)
