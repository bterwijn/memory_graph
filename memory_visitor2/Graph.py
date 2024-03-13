import graphviz
import utils

from Memory_Visitor import Memory_Visitor

class Graph:

    def __init__(self, data, 
                 graph_attr={}, 
                 node_attr={'shape':'plaintext'}, 
                 edge_attr={}):
        self.new_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graph_attr,
                                    node_attr=node_attr,
                                    edge_attr=edge_attr)
        memory_visitor = Memory_Visitor(self.backtrack_callback)
        memory_visitor.visit(data)

    def backtrack_callback(self, node):
        print("backtrack categorized:",node)
        node.add_to_graph(self)
        
    def add_node(self, node_name, node_html, node_label):
        print('add_node:', node_name, node_html, node_label)
        self.new_graph.node(node_name,
                            node_html,
                            xlabel=node_label)

    def get_graph(self):
        return self.new_graph
    

if __name__ == '__main__':
    data = utils.nested_list([4,4,4])
    print(data)
    graph = Graph(data)
    graph.get_graph().render(outfile='graph.png')
    # import test
    # test_fun_count=0
    # def test_fun(data):
    #     global test_fun_count
    #     graph_builder = Graph_Builder(data)
    #     new_graph = graph_builder.get_graph()
    #     new_graph.render(outfile=f'test_graph{test_fun_count}.png')
    #     test_fun_count += 1
    # test.test_all( test_fun )