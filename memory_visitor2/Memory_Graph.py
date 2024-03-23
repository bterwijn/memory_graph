import graphviz
import utils
import config_helpers

from Slicer import Slicer
from Memory_Visitor import Memory_Visitor
from Node import Node

import test # last

class Memory_Graph:

    def __init__(self, data, 
                 colors = None,
                 vertical_orientations = None,
                 slicers = None,
                 graphviz_graph_attr = {}, 
                 graphviz_node_attr = {'shape':'plaintext'}, 
                 graphviz_edge_attr = {}
                 ):
        self.subgraphed_nodes = set()
        self.new_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graphviz_graph_attr,
                                    node_attr=graphviz_node_attr,
                                    edge_attr=graphviz_edge_attr)
        memory_visitor = Memory_Visitor(self.backtrack_callback)
        config_helpers.set_config(colors, vertical_orientations, slicers) # TODO: not happy, Memory_Visitor also set_configs
        memory_visitor.visit(data)

    def backtrack_callback(self, node):
        #print("backtrack node:",node)
        color = config_helpers.get_color(node)
        border = 3 if node.get_parent() is None else 1
        html_table = node.get_html_table()
        self.new_graph.node(node.get_name(),
                            html_table.to_string(border, color),
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
        graph = Memory_Graph(data) #, colors={id(data):'red'}, vertical_orientations={id(data):True, list:False}, slicers={id(data):(Slicer(0,0),Slicer(0,0))} )
        graph.get_graph().render(outfile=f'test_graph{test_fun_count}.png')
        test_fun_count += 1
    test.test_all(test_fun)
