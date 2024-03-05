import graphviz
import memory_visitor
import node_layout
import utils

class Graph_Builder:

    def __init__(self, data, 
                 graph_attr={}, 
                 node_attr={'shape':'plaintext'}, 
                 edge_attr={}):
        self.new_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graph_attr,
                                    node_attr=node_attr,
                                    edge_attr=edge_attr)
        self.subgraphed_ids = set()
        memory_visitor.visit_callback = self.visit_callback
        memory_visitor.visit_backtrack_callback = self.backtrack_callback
        memory_visitor.visit(data)

    def set_subgraphed(self,data):
        self.subgraphed_ids.add(id(data))
        return data
    
    def is_subgraphed(self,data):
        return id(data) in self.subgraphed_ids
    
    def visit_callback(self,categorized,parent):
        #print("visit data:",data,"testparent:",parent)
        pass

    def backtrack_callback(self,categorized):
        print("backtrack categorized:",categorized)
        node_name = categorized.get_node_name()
        # subgraph
        subgraph_children = [memory_visitor.get_node_name(self.set_subgraphed(c)) 
                            for c in categorized.get_children() if not self.is_subgraphed(c)]
        if len(subgraph_children) > 1:
            self.new_graph.body.append(node_layout.make_subgraph(subgraph_children))
        # node
        self.new_graph.node(node_name, 
                            categorized.get_body(),
                            xlabel=categorized.get_type_name())
        # edges
        for i,c in enumerate(categorized.get_children()):
            self.new_graph.edge(f'{node_name}:f{i}',
                                f'{memory_visitor.get_node_name(c)}:X')

    def get_graph(self):
        return self.new_graph

class My_Class:

    def __init__(self):
        self.a=10
        self.b=20
        self.c=30


if __name__ == '__main__':
    data = 100
    data = [ 1, 2, 3, 4 ]
    data = [[1,2],[3,4]]
    #data = {1:10, 2:20, 3:30}
    data = (My_Class())
    graph_builder = Graph_Builder(data)
    graph = graph_builder.get_graph()
    graph.view()
    #new_graph.render(outfile='what.gv')

