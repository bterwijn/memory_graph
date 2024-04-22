

class Sliced_Graph:

    def __init__(self, full_graph, slicer) -> None:
        self.full_graph = full_graph
        self.slicer = slicer
        self.parents = {}
        self.slice(full_graph.get_root())

    def __repr__(self) -> str:
        s = "Sliced_Graph\n=== parents:\n"
        for parent_id in self.parents:
            s += f"{parent_id} : {self.get_slices(parent_id)} {self.full_graph.get_node(parent_id)}\n"
        return s

    def slice(self, data_id):
        if data_id in self.parents:
            return
        node = self.full_graph.get_node(data_id)
        children = node.get_children()
        if not children is None:
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

    def process_nodes(self, callback):
        self.process_nodes_recursive(self.full_graph.get_root(), callback, set())

    def process_nodes_recursive(self, node_id, callback, id_to_count):
        node = self.full_graph.get_node(node_id)
        node_id = id(node.get_data())
        if not node_id in id_to_count:
            node_count = len(id_to_count)
            id_to_count.add(node_id)
            children = node.get_children()
            slices = None
            if not children is None:
                slices = self.get_slices(node_id)
                for slice in slices.get_slices():
                    for child in node.get_children()[slice[0]:slice[1]]:
                        self.process_nodes_recursive(child, callback, id_to_count)
            callback(node_count, node, slices)
