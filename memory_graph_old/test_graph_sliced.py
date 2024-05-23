from memory_graph.graph_full import Graph_Full
from memory_graph.graph_sliced import Graph_Sliced

import memory_graph.config_default
import memory_graph.config_helpers

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
    memory_graph.config_helpers.set_config()
    a = [1,2]
    b = [3,4,a]
    c = [5,6,b]
    d = [7,8,c]
    long_list = [i for i in range(30)]
    long_list[8] = d
    long_list[10] = b
    data = [long_list, a]
    graph_full = Graph_Full(data)
    graph_sliced = Graph_Sliced(graph_full)
    print('graph_sliced:',graph_sliced)
    graph_sliced.add_missing_edges()