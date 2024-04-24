from memory_graph.Memory_Visitor import Memory_Visitor
from memory_graph.Full_Graph import Full_Graph
from memory_graph.Sliced_Graph import Sliced_Graph
from memory_graph.Slicer import Slicer

import memory_graph.config as config
import memory_graph.config_helpers as config_helpers

import graphviz

class Memory_Graph:
    """
    Memory_Graph creates a graph of memory using the graphviz library. 
    """

    def __init__(self, data, 
                 colors = None,
                 vertical_orientations = None,
                 slicers = None,
                 graphviz_graph_attr = {}, 
                 graphviz_node_attr = {'shape':'plaintext'}, 
                 graphviz_edge_attr = {}
                 ):
        """ 
        Create a graph of memory using the graphviz library.

        Args:
            data (Node): The root node of the memory in the graph.
            colors (dict): A dictionary of colors to use for different types of nodes.
            vertical_orientations (dict): A dictionary of whether to use vertical/horizontal orientation for different types of nodes.
            slicers (dict): A dictionary of slicers to use for different types of nodes.
            graphviz_graph_attr (dict): A dictionary of graph attributes used to configure graphviz.
            graphviz_node_attr (dict): A dictionary of node attributes used to configure graphviz.
            graphviz_edge_attr (dict): A dictionary of edge attributes used to configure graphviz.
        """
        config_helpers.set_config()
        self.subgraphed_nodes = set()
        self.new_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graphviz_graph_attr,
                                    node_attr=graphviz_node_attr,
                                    edge_attr=graphviz_edge_attr)
        
        full_graph = Full_Graph(data)
        print(full_graph)
        sliced_graph = Sliced_Graph(full_graph, Slicer(2,2))
        print(sliced_graph)
        sliced_graph.add_missing_edges()
        print(sliced_graph)
        sliced_graph.process_nodes(self.node_callback)

    def node_callback(self, node, slices, full_graph):
        if not node.get_type() in config.no_reference_types or node.get_id() == full_graph.get_root_id() :
            print('node:', node,'slices:', slices)
            html_table = node.get_html_table(slices, full_graph)
            edges = html_table.get_edges()
            # ------------ subgraph
            self.add_subgraph(edges)
            # ------------ node
            color = config_helpers.get_color(node)
            border = 3 if node.get_id() == full_graph.get_root_id() else 1
            self.new_graph.node(node.get_name(),
                                html_table.to_string(border, color),
                                xlabel=node.get_label())
            # ------------ edges
            for parent,child in edges:
                self.new_graph.edge(parent, child+':table')

    def backtrack_callback(self, node):
        """
        Callback function called by the Memory_Visitor when backtracking while reading each 
        node in the memory reachable from the 'data' root node after calling the Memory_Graph constructor.
        """
        #print("backtrack node:",node)
        html_table = node.get_html_table()
        edges = html_table.get_edges()
        # ------------ subgraph
        self.add_subgraph(edges)
        # ------------ node
        color = config_helpers.get_color(node)
        border = 3 if node.get_parent() is None else 1
        self.new_graph.node(node.get_name(),
                            html_table.to_string(border, color),
                            xlabel=node.get_label())
        # ------------ edges
        for parent,child in edges:
            self.new_graph.edge(parent, child+':table')

    def add_subgraph(self, edges):
        """
        Helper function to add 'edges' to the graphviz graph. Each edges is a tuple (parent,child) where parent 
        and child are node names. Each edge is added to the graph only once.
        """
        new_edges = [child for _,child in edges if child not in self.subgraphed_nodes]
        if len(new_edges) > 1:
            self.new_graph.body.append('{ rank="same"  '+(" -> ".join(new_edges))+'  [weight=99,style=invis]; }\n')
        for c in new_edges:
            self.subgraphed_nodes.add(c)

    def get_graph(self):
        """
        Returns the graphviz graph constructed after calling the Memory_Graph constructor.
        """
        return self.new_graph
