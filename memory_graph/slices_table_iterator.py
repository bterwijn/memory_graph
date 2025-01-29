# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from abc import ABC, abstractmethod

class Slices_Table_Iterator(ABC):
    
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

class Slices_Table_Iterator1D(Slices_Table_Iterator):

    def __init__(self, slices1d, size):
        self.slices = slices1d
        self.size = size
        self.gen = self.generate()

    def __iter__(self):
        return self

    def generate(self):
        slices = self.slices.get_slices()
        if len(slices) > 0 and slices[0][0] > 0:
            yield -1
        for slice in slices:
            for i in range(slice[0], slice[1]):
                yield i
            if i < self.size-1:
                yield -1

    def __next__(self):
        return next(self.gen)
    
class Slices_Table_Iterator2D(Slices_Table_Iterator):

    def __init__(self, slices2d, size):
        self.slices = slices2d
        self.size = size
        self.gen = self.generate()

    def __iter__(self):
        return self

    def generate(self):
        row_slices = self.slices.get_row_slices().get_slices()
        col_slices = self.slices.get_col_slices().get_slices()
        first_row_slice = True
        for row_slice in row_slices:
            if first_row_slice:
                if len(row_slices) > 0 and row_slice[0] > 0:
                    yield (-3, -3)
                first_col_slice = False
            else:
                yield (-3, -3)
            for row_i in range(row_slice[0], row_slice[1]):
                first_col_slice = True
                for col_slice in col_slices:
                    if first_col_slice:
                        if len(col_slices) > 0 and col_slice[0] > 0:
                            yield (row_i, -1)
                        first_col_slice = False
                    else:
                        yield (row_i, -1)  
                    for col_i in range(col_slice[0], col_slice[1]):
                        yield (row_i, col_i)
                if col_i < self.size[1]-1:
                    yield (row_i, -1)
                yield (row_i, -2)
        if len(row_slices)>0 and row_i < self.size[0]-1:
            yield (row_i, -3)

    def __next__(self):
        return next(self.gen)
