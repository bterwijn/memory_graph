import memory_graph.config_helpers

class Sliced_Graph:

    def __init__(self, full_graph) -> None:
        self.full_graph = full_graph
        self.id_to_slices = {}
        self.slice(full_graph.get_root_id())

    def __repr__(self) -> str:
        s = "Sliced_Graph\n=== parents:\n"
        for node_id in self.id_to_slices:
            s += f"{node_id} : {self.get_slices(node_id)} {self.full_graph.get_node(node_id)}\n"
        return s

    def slice(self, node_id):
        if node_id in self.id_to_slices:
            return
        node = self.full_graph.get_node(node_id)
        children = node.get_children()
        if not children is None:
            slicer = memory_graph.config_helpers.get_slicer_1d(node, node.get_data())
            slices = slicer.get_slices(len(children))
            self.id_to_slices[node_id] = slices
            try:
                for slice in slices.get_slices():
                    for child in children[slice[0]:slice[1]]:
                        self.slice(id(child))
            except TypeError:
                slices.slice_iterable(children, lambda child: self.slice(id(child)))

    def get_node_ids(self):
        return self.id_to_slices
    
    def get_slices(self, node_id):
        return self.id_to_slices[node_id]
    
    def add_missing_edges(self):
        for node_id in self.get_node_ids():
            print("node_id:", node_id)
            self.add_paths_to_root(node_id)

    def add_paths_to_root(self, node_id):
        print('  node_id:',node_id)
        parents_indices = self.full_graph.get_parents(node_id)
        for parent, indices in parents_indices.items():
            for index in indices:
                print('    parent:',parent,'index:',index)
                slices = self.get_slices(parent)
                slices.add_slice([index,index+1], 0) 
            if not parent in self.id_to_slices:
                self.add_paths_to_root(parent)

    def process_nodes(self, callback):
        self.process_nodes_recursive(self.full_graph.get_root_id(), callback, set())

    def process_nodes_recursive(self, node_id, callback, id_to_count):
        if not node_id in id_to_count:
            id_to_count.add(node_id)
            node = self.full_graph.get_node(node_id)
            children = node.get_children()
            slices = None
            if not children is None:
                slices = self.get_slices(node_id)
                for slice in slices.get_slices():
                   for child in node.get_children()[slice[0]:slice[1]]:
                       self.process_nodes_recursive(id(child), callback, id_to_count)
            callback(node, slices, self.full_graph)
