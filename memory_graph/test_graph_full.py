from memory_graph.graph_full import Graph_Full

class My_Class:

    def __init__(self) -> None:
        self.a = 100
        self.b = 200

    def __repr__(self) -> str:
        return f"My_Class({self.a},{self.b})"

def walk_graph(graph_full, element_id, indent=0):
    element = graph_full.get_element_by_id(element_id)
    children = graph_full.get_children(element)
    print(' '*indent, 'element:', element)
    print(' '*indent, 'data:', graph_full.get_data(element))
    print(' '*indent, 'parent_indices:', graph_full.get_parent_indices_by_id(element_id))
    print(' '*indent, 'children:', children)
    if not children is None:
        for child in children:
            child_id = id(child)
            walk_graph(graph_full, child_id, indent+2)

if __name__ == '__main__':
    data = [[1,2],(3,4), {5:500, 6:600}, My_Class()]
    graph_full = Graph_Full(data)
    print('graph_full:',graph_full)
    walk_graph(graph_full, graph_full.get_root_id())
