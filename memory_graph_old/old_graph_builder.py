from memory_graph.graph_full import Graph_Full
from memory_graph.graph_sliced import Graph_Sliced
import memory_graph.graph_sliced 
from memory_graph.element_key_value import Element_Key_Value

import memory_graph.config as config
import memory_graph.config_helpers as config_helpers

import graphviz

class Graph_Builder:
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
            data (Element_Base): The root node of the memory in the graph.
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
        
        graph_full = Graph_Full(data)
        #print(graph_full)
        graph_sliced = Graph_Sliced(graph_full, depth = config.max_tree_depth)
        #print(graph_sliced)
        graph_sliced.add_missing_edges()
        #print(graph_sliced)
        graph_sliced.visit_all_nodes(self.node_callback)

    def node_callback(self, node, slices, graph_sliced):
        graph_full = graph_sliced.get_graph_full()
        print('node:', node,'slices:', slices)
        html_table = node.get_html_table(slices, graph_sliced)
        edges = html_table.get_edges()
        # ------------ subgraph
        self.add_subgraph(edges)
        # ------------ node
        color = config_helpers.get_color(node)
        border = 3 if id(node) == graph_full.get_root_id() else 1
        self.new_graph.node(node.get_name(),
                            html_table.to_string(border, color),
                            xlabel=node.get_label(slices))
        # ------------ edges
        for parent,child,dashed in edges:
            self.new_graph.edge(parent, child+':table', style='dashed' if dashed else 'solid')

    def add_subgraph(self, edges):
        """
        Helper function to add 'edges' to the graphviz graph. Each edges is a tuple (parent,child) where parent 
        and child are node names. Each edge is added to the graph only once.
        """
        new_edges = [child for _,child,_ in edges if child not in self.subgraphed_nodes]
        if len(new_edges) > 1:
            self.new_graph.body.append('{ rank="same"  '+(" -> ".join(new_edges))+'  [weight=99,style=invis]; }\n')
        for c in new_edges:
            self.subgraphed_nodes.add(c)

    def get_graph(self):
        """
        Returns the graphviz graph constructed after calling the Memory_Graph constructor.
        """
        return self.new_graph
