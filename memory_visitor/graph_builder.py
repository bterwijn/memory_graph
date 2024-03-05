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
        memory_visitor.visit_callback = self.visit_callback
        memory_visitor.visit_backtrack_callback = self.backtrack_callback
        memory_visitor.visit(data)
    
    def visit_callback(self,categorized,parent):
        #print("visit data:",data,"testparent:",parent)
        pass

    def backtrack_callback(self,categorized):
        print("backtrack categorized:",categorized)
        node_name = categorized.get_node_name()
        # === subgraph
        subgraph = node_layout.make_subgraph(categorized.get_children())
        if subgraph:
            self.new_graph.body.append(subgraph)
        # === node
        self.new_graph.node(node_name, 
                            categorized.get_body(),
                            xlabel=categorized.get_type_name())
        # === edges
        for i,c in enumerate(categorized.get_children()):
            self.new_graph.edge(f'{node_name}:f{i}',
                                f'{c.get_node_name()}:X')

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
