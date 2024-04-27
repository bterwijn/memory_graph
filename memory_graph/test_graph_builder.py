from memory_graph.graph_builder import Graph_Builder

import memory_graph.config_default as config_default
import memory_graph.test as test

if __name__ == '__main__':
    test_fun_count = 0
    def test_fun(data):
        global test_fun_count
        graph = Graph_Builder(data) #, colors={id(data):'red'}, vertical_orientations={id(data):True, list:False}, slicers={id(data):(Slicer(0,0),Slicer(0,0))} )
        graph.get_graph().render(outfile=f'test_graph{test_fun_count}.png')
        test_fun_count += 1
    test.test_all(test_fun)
