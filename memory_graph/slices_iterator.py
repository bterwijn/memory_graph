# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause


from abc import ABC, abstractmethod

class Slices_Iterator(ABC):
    
    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def __next__(self):
        pass

class Slices_Iterator1D(Slices_Iterator):

    def __init__(self, slices1d):
        self.slices = slices1d
        self.gen = self.generate()

    def __iter__(self):
        return self

    def generate(self):
        slices = self.slices.get_slices()
        for si in range(len(slices)):
            for i in range(slices[si][0], slices[si][1]):
                yield i

    def __next__(self):
        return next(self.gen)
    
class Slices_Iterator2D(Slices_Iterator):

    def __init__(self, slices2d):
        self.slices = slices2d
        self.gen = self.generate()

    def __iter__(self):
        return self

    def generate(self):
        row_slices = self.slices.get_row_slices().get_slices()
        col_slices = self.slices.get_col_slices().get_slices()
        for row_slice in row_slices:
            for row_i in range(row_slice[0], row_slice[1]):
                for col_slice in col_slices:
                    for col_i in range(col_slice[0], col_slice[1]):
                        yield (row_i, col_i)

    def __next__(self):
        return next(self.gen)
