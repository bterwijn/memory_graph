from abc import ABC, abstractmethod

import bisect
import copy

from memory_graph.slices_iterator import Slices_Iterator1D, Slices_Iterator2D
from memory_graph.slices_table_iterator import Slices_Table_Iterator1D, Slices_Table_Iterator2D

class Slices(ABC):

    @abstractmethod
    def __iter__(self):
        pass

    @abstractmethod
    def add_index(self, index):
        pass

    @abstractmethod
    def table_iter(self, size):
        pass

class Slices1D(Slices):

    def __init__(self, slices=None) -> None:
        self.slices = []
        if not slices is None:
            for i in slices:
                self.add_slice(i)

    def __repr__(self) -> str:
        return f"Slices1D({self.slices})"
    
    def get_iter(self,length):
        return Slices_Iterator(self.slices,length)

    def copy(self):
        s = Slices1D()
        s.slices = copy.deepcopy(self.slices)
        return s

    def get_slices(self):
        return self.slices

    def add_slice(self, begin_end, remove_interposed_dots=1):
        insert0 = bisect.bisect_right(self.slices, begin_end[0], key=lambda x: x[0])
        insert1 = bisect.bisect_left (self.slices, begin_end[1], key=lambda x: x[1])
        merge_begin, merge_end = False, False
        if insert0 > 0:
            if self.slices[insert0-1][1] >= (begin_end[0] - remove_interposed_dots):
                merge_begin = True
        if insert1 < len(self.slices):
            if self.slices[insert1][0] <= (begin_end[1] + remove_interposed_dots):
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
    
    def add_index(self, index):
        self.add_slice([index,index+1], 0)
    
    def table_iter(self, size):
        return Slices_Table_Iterator1D(self, size)

class Slices2D(Slices):

    def __init__(self, row_slices = None, col_slices= None) -> None:
        self.row_slices = Slices1D() if row_slices is None else row_slices
        self.col_slices = Slices1D() if col_slices is None else col_slices

    def __repr__(self):
        s='Sices2D:\n'
        s += 'row_slices:' + str(self.row_slices) + '\n'
        s += 'col_slices:' + str(self.col_slices) + '\n'
        return s
    
    def get_row_slices(self):
        return self.row_slices
    
    def get_col_slices(self):
        return self.col_slices

    def __iter__(self):
        return Slices_Iterator2D(self)

    def add_index(self, index):
        i0,i1 = index
        self.row_slices.add_slice([i0,i0+1], 0)
        self.col_slices.add_slice([i1,i1+1], 0)

    def table_iter(self, size):
        return Slices_Table_Iterator2D(self, size)
