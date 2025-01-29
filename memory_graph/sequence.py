# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from abc import ABC, abstractmethod

from memory_graph.slices import Slices1D, Slices2D
import memory_graph.utils as utils

class Sequence(ABC):

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def size(self):
        pass

    @abstractmethod
    def empty_slices(self):
        pass

    @abstractmethod
    def slice(self, slicer):
        pass

    @abstractmethod
    def indices_all(self):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    @abstractmethod
    def __setitem__(self, index, value):
        pass

class Sequence1D(Sequence):

    def __init__(self, data):
        self.data = utils.make_sliceable(data)

    def __repr__(self):
        return f'Sequence1D: {self.data}'
    
    def is_empty(self):
        return len(self.data) == 0
    
    def size(self):
        return len(self.data)
    
    def empty_slices(self):
        return Slices1D()

    def slice(self, slicer):
        return slicer.get_slices( len(self.data) )

    def indices_all(self):
        for i in range(len(self.data)):
            yield i

    def __getitem__(self, index):
        return self.data[index]
    
    def __setitem__(self, index, value):
        self.data[index] = value

class Sequence2D(Sequence):

    def __init__(self, data):
        self.data = utils.make_sliceable(data)

    def __repr__(self):
        return f'Sequence2D: {self.data}'
    
    def is_empty(self):
        return len(self.data) == 0

    def size(self):
        l1, l2 = len(self.data), 0
        if l1 > 0:
            l2 = len(self.data[0])
        return l1, l2
    
    def empty_slices(self):
        return Slices2D()

    def slice(self, slicer0):
        if type(slicer0) is tuple:
            slicer0, slicer1 = slicer0
        else:
            slicer1 = slicer0
        slices0 = slicer0.get_slices( len(self.data) )
        slices1 = slicer1.get_slices( len(self.data[0]) )
        return Slices2D(slices0, slices1)

    def indices_all(self):
        len0 = len(self.data) 
        if len0 > 0:
            len1 = len(self.data[0])
            for y in range(len0):
                for x in range(len1):
                    yield (y,x)

    def __getitem__(self, index):
        return self.data[index[0]][index[1]]

    def __setitem__(self, index, value):
        self.data[index[0]][index[1]] = value
