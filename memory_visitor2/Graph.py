import graphviz
import utils
import test

from Memory_Visitor import Memory_Visitor
from Node import Node

class Graph:

    def __init__(self, data, 
                 graph_attr={}, 
                 node_attr={'shape':'plaintext'}, 
                 edge_attr={}):
        self.new_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graph_attr,
                                    node_attr=node_attr,
                                    edge_attr=edge_attr)
        self.subgraphed_nodes = set()
        memory_visitor = Memory_Visitor(self.backtrack_callback)
        memory_visitor.visit(data)

    def backtrack_callback(self, node):
        #print("backtrack node:",node)
        html_table = node.get_html_table()
        self.new_graph.node(node.get_name(),
                            html_table.to_string(),
                            xlabel=node.get_label())
        edges = html_table.get_edges()
        for node,child in edges:
            self.new_graph.edge(node, child+':table')
        self.add_subgraph(edges)

    def add_subgraph(self, edges):
        new_edges = [child for node,child in edges if child not in self.subgraphed_nodes]
        if len(new_edges) > 1:
            for c in new_edges:
                self.subgraphed_nodes.add(c)
            self.new_graph.body.append('{ rank="same"  '+(" -> ".join(new_edges))+'  [weight=99,style=invis]; }\n')

    def get_graph(self):
        return self.new_graph
    
if __name__ == '__main__':
    test_fun_count = 0
    def test_fun(data):
        global test_fun_count
        graph = Graph(data)
        graph.get_graph().render(outfile=f'test_graph{test_fun_count}.png')
        test_fun_count += 1
    test.test_all(test_fun)
