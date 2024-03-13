import graphviz
import utils

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
        memory_visitor = Memory_Visitor(self.backtrack_callback)
        memory_visitor.visit(data)

    def backtrack_callback(self, node):
        print("backtrack categorized:",node)

        self.new_graph.node(node.get_name(),
                            str(node.get_html_table()),
                            xlabel=node.get_label())
        for node,child in node.get_edges():
            self.new_graph.edge(node.get_name(), child.get_name())
        #node.add_to_graph(self)   

    def get_graph(self):
        return self.new_graph
    

if __name__ == '__main__':
    data = utils.nested_list([5,4])
    print(data)
    graph = Graph(data)
    graph.get_graph().render(outfile='graph.png')
   