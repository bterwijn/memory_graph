import graphviz
import memory_visitor
import node_layout

class Graph_Builder:

    def __init__(self, data, 
                 graph_attr={}, 
                 node_attr={'shape':'plaintext'}, 
                 edge_attr={}):
        self.new_graph=graphviz.Digraph('memory_graph',
                                    graph_attr=graph_attr,
                                    node_attr=node_attr,
                                    edge_attr=edge_attr)
        self.is_subgraphed = set()
        self.references = []
        memory_visitor.visit_callback = self.visit_callback
        memory_visitor.visit_backtrack_callback = self.backtrack_callback
        memory_visitor.visit(data)

    def get_name(self,data):
        return "node"+str(memory_visitor.get_id(data))

    def set_subgraphed(self,data):
        self.is_subgraphed.add(data)
        return data

    def visit_callback(self,data,parent):
        #print("visit data:",data,"testparent:",parent)
        pass

    def backtrack_callback(self,data,children):
        print("backtrack data:",data,"children:",children)
        # subgraph
        subgraph_chidren = [self.get_name(self.set_subgraphed(c)) 
                    for c in children if c not in self.is_subgraphed]
        if len(subgraph_chidren) > 1:
            subgraph = node_layout.make_subgraph(subgraph_chidren)
            print('subgraph:',subgraph)
            self.new_graph.body.append(subgraph)
        # node
        name = self.get_name(data)
        body = node_layout.make_node_body(data,children)
        type = node_layout.get_type_name(data)
        print('name:',name,'type:',type)
        self.new_graph.node(self.get_name(data), 
                            body, 
                            xlabel=node_layout.get_type_name(data))

    def get_graph(self):
        return self.new_graph

if __name__ == '__main__':
    data = [1,2]
    graph_builder = Graph_Builder(data)
    graph = graph_builder.get_graph()
    graph.view()
    #new_graph.render(outfile='what.gv')

