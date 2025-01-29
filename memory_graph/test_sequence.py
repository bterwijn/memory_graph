# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from memory_graph.sequence import Sequence1D, Sequence2D
from memory_graph.slicer import Slicer

def status(index):
    if type(index) == tuple:
        return index[0]
    return index

def test_slicing(sequence, slicer):
    print(sequence)
    print(slicer)
    for i in sequence.indices_all():
        print(i, sequence[i])
    slices = sequence.slice(slicer)
    print('slices:',slices)
    for index in slices:
        print(index, ':', sequence[index])
    for index in slices.table_iter(sequence.size()):
        print(f'{index}: {sequence[index] if status(index)>=0 else None}')

def test_sequence():
    sequence = Sequence1D([i for i in range(8)])
    slicer = Slicer(2,3)
    test_slicing(sequence, slicer)

    width = 5
    height = 6
    sequence = Sequence2D([[x+y*width for x in range(width)] for y in range(height)])
    slicer = (Slicer(1,2), Slicer(2,1))
    test_slicing(sequence, slicer)

if __name__ == '__main__':
    test_sequence()
