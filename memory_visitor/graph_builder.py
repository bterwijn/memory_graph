import graphviz
import memory_visitor
import node_layout
import utils
import test

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


if __name__ == '__main__':
    test_fun_count=0
    def test_fun(data):
        global test_fun_count
        graph_builder = Graph_Builder(data)
        new_graph = graph_builder.get_graph()
        new_graph.render(outfile=f'test_graph{test_fun_count}.png')
        test_fun_count += 1

    test.test_all( test_fun )
