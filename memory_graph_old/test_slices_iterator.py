
from memory_graph.slices_iterator import Slices_Iterator1D, Slices_Iterator2D
from memory_graph.slices import Slices1D, Slices2D

def test_slices_iterator1d():
    
    slices1d = Slices1D( [[10,20], [30,40], [60,70], [80,90]] )
    iter = Slices_Iterator1D(slices1d)
    for i in iter:
        print(i)
    assert list(Slices_Iterator1D(slices1d)) == [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89], "Slices_Iterator: Error in iteration"

def test_slices_iterator2d():
    
    slices2d = Slices2D( [(0, Slices1D( [[10,20], [30,40]] )),
                          (1, Slices1D( [[10,20], [60,70]] )),
                          ] )
    iter = Slices_Iterator2D(slices2d)
    for i in iter:
        print(i)

    assert list(Slices_Iterator2D(slices2d)) == [(0, 10), (0, 11), (0, 12), (0, 13), (0, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (0, 30), (0, 31), (0, 32), (0, 33), (0, 34), (0, 35), (0, 36), (0, 37), (0, 38), (0, 39), (0, 60), (0, 61), (0, 62), (0, 63), (0, 64), (0, 65), (0, 66), (0, 67), (0, 68), (0, 69), (1, 10), (1, 11), (1, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 30), (1, 31), (1, 32), (1, 33), (1, 34), (1, 35), (1, 36), (1, 37), (1, 38), (1, 39), (1, 60), (1, 61), (1, 62), (1, 63), (1, 64), (1, 65), (1, 66), (1, 67), (1, 68), (1, 69)], "Slices_Iterator: Error in iteration"

if __name__ == '__main__':
    test_slices_iterator1d()
    test_slices_iterator2d()
    print("Slices_Iterator: All tests pass")    