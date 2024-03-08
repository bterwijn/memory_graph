
class Subgraph:

    def __init__(self):
        self.children = []

    def add_child(self, child):
        if not child.is_subgraphed():
            child.set_subgraphed()
            self.children.append(f'{child.get_node_name()}:X')

    def add_subgraph(self, graph):
        if len(self.children) > 1:
            graph.body.append('{ rank="same"  '+(" -> ".join(self.children))+'  [weight=99,style=invis]; }\n')

class Node_Builder:

    def __init__(self,graph):
        self.graph = graph
        self.entry_count = 0
        self.ref_count = 0
        self.subgraph = Subgraph()

    def make_table_entry(self, categorized, child, fun_str, fun_ref):
        if type(child) == str:
            entry = fun_str(child)
        else:
            field = f'f{self.entry_count}'
            entry = fun_ref(field)
            cname = f'{child.get_node_name()}:X'
            self.graph.edge(f'{categorized.get_node_name()}:{field}', cname)
            self.subgraph.add_child(child)
            self.ref_count += 1
        self.entry_count += 1
        return entry

    def write_subgraph(self):
        self.subgraph.add_subgraph(self.graph)

    def get_ref_count(self):
        return self.ref_count
    
