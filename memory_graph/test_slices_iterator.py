# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause


from memory_graph.slices_iterator import Slices_Iterator1D, Slices_Iterator2D
from memory_graph.slices import Slices1D, Slices2D

def test_slices_iterator1d():
    slices1d = Slices1D( [[10,20], [30,40], [60,70], [80,90]] )
    iter = Slices_Iterator1D(slices1d)
    for i in iter:
        print(i)
    assert list(Slices_Iterator1D(slices1d)) == [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89], "Slices_Iterator: Error in iteration"

def test_slices_iterator2d():
    slices2d = Slices2D( Slices1D( [[10,12], [20,22]] ),
                         Slices1D( [[10,12], [30,32]] )  )
    iter = Slices_Iterator2D(slices2d)
    for i in iter:
        print(i)
    assert list(Slices_Iterator2D(slices2d)) == [(10, 10), (10, 11), (10, 30), (10, 31), (11, 10), (11, 11), (11, 30), (11, 31), (20, 10), (20, 11), (20, 30), (20, 31), (21, 10), (21, 11), (21, 30), (21, 31)]


if __name__ == '__main__':
    test_slices_iterator1d()
    test_slices_iterator2d()
    print("Slices_Iterator: All tests pass")
