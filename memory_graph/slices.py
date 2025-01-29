# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from abc import ABC, abstractmethod

import bisect
import copy

from memory_graph.slices_iterator import Slices_Iterator1D, Slices_Iterator2D
from memory_graph.slices_table_iterator import Slices_Table_Iterator1D, Slices_Table_Iterator2D

class Slices(ABC):

    def __init__(self):
        self.dashed = set()

    def __repr__(self) -> str:
        return f"dashed: {self.dashed}"

    def is_dashed(self, index):
        return index in self.dashed

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def has_index(self, index):
        pass

    @abstractmethod
    def add_index(self, index):
        pass

    @abstractmethod
    def table_iter(self, size):
        pass

    @abstractmethod
    def is_empty(self):
        pass

class Slices1D(Slices):

    def __init__(self, slices=None) -> None:
        super().__init__()
        self.slices = []
        if not slices is None:
            for i in slices:
                self.add_slice(i)

    def __repr__(self) -> str:
        return f"Slices1D({self.slices}) "+super().__repr__()
    
    def get_iter(self,length):
        return Slices_Iterator(self.slices,length)

    def copy(self):
        s = Slices1D()
        s.slices = copy.deepcopy(self.slices)
        s.dashed = copy.deepcopy(self.dashed)
        return s

    def get_slices(self):
        return self.slices

    def has_index(self, index):
        for i in self.slices:
            if i[0] <= index and index < i[1]:
                return True
        return False

    def add_slice(self, begin_end, remove_interposed_dots=1):
        i0, i1 = begin_end
        if i1 <= i0:
            return False
        insert0 = bisect.bisect_right(self.slices, i0, key=lambda x: x[0])
        insert1 = bisect.bisect_left (self.slices, i1, key=lambda x: x[1])
        merge_begin, merge_end = False, False
        if insert0 > 0:
            if self.slices[insert0-1][1] >= (i0 - remove_interposed_dots):
                merge_begin = True
        if insert1 < len(self.slices):
            if self.slices[insert1][0] <= (i1 + remove_interposed_dots):
                merge_end = True
        if merge_begin and merge_end:
            if insert0 - insert1 == 1: # no slices changed
                return False
            self.slices[insert0-1][1] = self.slices[insert1][1]
            del self.slices[insert0:insert1+1]
        elif merge_begin:
            self.slices[insert0-1][1] = max(self.slices[insert1-1][1], begin_end[1])
            del self.slices[insert0:insert1]
        elif merge_end:
            self.slices[insert1][0] = min(self.slices[insert0][0], begin_end[0])
            del self.slices[insert0:insert1]
        else:
            del self.slices[insert0:insert1]
            self.slices.insert(insert0, begin_end)
        return True
    
    def __iter__(self):
        return Slices_Iterator1D(self)
    
    def has_index(self, index):
        insert = bisect.bisect_right(self.slices, index, key=lambda x: x[0])
        #print('insert:',insert,'index:',index,'slices:',self.slices)
        if insert==0:
            return False
        i0, i1 = self.slices[insert-1]
        return i0 <= index and index < i1

    def add_index(self, index, dashed=False):
        self.add_slice([index,index+1], 0)
        if dashed:
            self.dashed.add(index)
    
    def table_iter(self, size):
        return Slices_Table_Iterator1D(self, size)
    
    def is_empty(self):
        return len(self.slices) == 0

class Slices2D(Slices):

    def __init__(self, row_slices = None, col_slices= None) -> None:
        super().__init__()
        self.row_slices = Slices1D() if row_slices is None else row_slices
        self.col_slices = Slices1D() if col_slices is None else col_slices

    def __repr__(self):
        s='Sices2D:\n'
        s += 'row_slices:' + str(self.row_slices) + '\n'
        s += 'col_slices:' + str(self.col_slices) + '\n'
        s += super().__repr__() + '\n'
        return s
    
    def get_row_slices(self):
        return self.row_slices
    
    def get_col_slices(self):
        return self.col_slices

    def __iter__(self):
        return Slices_Iterator2D(self)

    def has_index(self, index):
        i0,i1 = index
        return self.row_slices.has_index(i0) and self.col_slices.has_index(i1)

    def add_index(self, index, dashed=False):
        i0,i1 = index
        self.row_slices.add_slice([i0,i0+1], 0)
        self.col_slices.add_slice([i1,i1+1], 0)
        if dashed:
            self.dashed.add((i0,i1))

    def table_iter(self, size):
        return Slices_Table_Iterator2D(self, size)

    def is_empty(self):
        return len(self.row_slices.slices) == 0
