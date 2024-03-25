
from Memory_Graph import Memory_Graph
import config_default
import test # last

if __name__ == '__main__':
    test_fun_count = 0
    def test_fun(data):
        global test_fun_count
        graph = Memory_Graph(data) #, colors={id(data):'red'}, vertical_orientations={id(data):True, list:False}, slicers={id(data):(Slicer(0,0),Slicer(0,0))} )
        graph.get_graph().render(outfile=f'test_graph{test_fun_count}.png')
        test_fun_count += 1
    test.test_all(test_fun)

