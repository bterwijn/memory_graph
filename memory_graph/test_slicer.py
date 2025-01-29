# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from memory_graph.slicer import Slicer

def test_slicer():
    slicer = Slicer(0.1, 0.2, 0.3)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [40, 60], [70, 100]], "Slicer error"

    slicer = Slicer(10, 20, 30)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [40, 60], [70, 100]], "Slicer error"

    slicer = Slicer(0.1, 0.3)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [70, 100]], "Slicer error"

    slicer = Slicer(10, 30)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [70, 100]], "Slicer error"

    slicer = Slicer(0.1)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10]], "Slicer error"

    slicer = Slicer(10)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10]], "Slicer error"

    slicer = Slicer()
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 100]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(0)
    assert slices.get_slices() == [], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(5)
    assert slices.get_slices() == [[0,5]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(6)
    assert slices.get_slices() == [[0,2],[4,6]], "Slicer error"

if __name__ == '__main__':
    test_slicer()
    print('Slicer test passed')
