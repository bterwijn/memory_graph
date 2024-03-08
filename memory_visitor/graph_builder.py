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
        memory_visitor.visit_backtrack_callback = self.backtrack_callback
        memory_visitor.visit(data)

    def backtrack_callback(self,categorized):
        #print("backtrack categorized:",categorized)
        categorized.add_to_graph(self.new_graph)

    def get_graph(self):
        return self.new_graph

if __name__ == '__main__':
    import test
    test_fun_count=0
    def test_fun(data):
        global test_fun_count
        graph_builder = Graph_Builder(data)
        new_graph = graph_builder.get_graph()
        new_graph.render(outfile=f'test_graph{test_fun_count}.png')
        test_fun_count += 1
    #test.test_linear( test_fun )   
    test.test_all( test_fun )
