from memory_graph.Memory_Graph import Memory_Graph

import memory_graph.config_default as config_default
import memory_graph.test as test

if __name__ == '__main__':
    test_fun_count = 0
    def test_fun(data):
        global test_fun_count
        graph = Memory_Graph(data) #, colors={id(data):'red'}, vertical_orientations={id(data):True, list:False}, slicers={id(data):(Slicer(0,0),Slicer(0,0))} )
        graph.get_graph().render(outfile=f'test_graph{test_fun_count}.png')
        test_fun_count += 1
    test.test_all(test_fun)

