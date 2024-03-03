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
        self.subgraphed_ids = set()
        memory_visitor.visit_callback = self.visit_callback
        memory_visitor.visit_backtrack_callback = self.backtrack_callback
        memory_visitor.visit(data)

    def get_name(self,data):
        return "node"+str(memory_visitor.get_id(data))

    def set_subgraphed(self,data):
        self.subgraphed_ids.add(id(data))
        return data
    
    def is_subgraphed(self,data):
        return id(data) in self.subgraphed_ids
    
    def visit_callback(self,data,parent):
        #print("visit data:",data,"testparent:",parent)
        pass

    def backtrack_callback(self,data,children):
        print("backtrack data:",data,"children:",children)
        # subgraph
        subgraph_chidren = [self.get_name(self.set_subgraphed(c)) 
                    for c in children if self.is_subgraphed(c)]
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
        # edges
        for i,c in enumerate(children):
            self.new_graph.edge(f'{self.get_name(data)}:f{i}',
                                f'{self.get_name(c)}:X')

    def get_graph(self):
        #self.new_graph.edge("node0:f0", "node1:X")
        return self.new_graph

class My_Class:

    def __init__(self):
        self.a=10
        self.b=20
        self.c=30

if __name__ == '__main__':
    #data = [[1,2],[3,4]]
    data = {1:10, 2:20, 3:30}
    data = My_Class()
    graph_builder = Graph_Builder(data)
    graph = graph_builder.get_graph()
    graph.view()
    #new_graph.render(outfile='what.gv')

