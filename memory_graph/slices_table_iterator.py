
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
        if self.size > 0:
            if slices[0][0] > 0:
                yield -1
        for si in range(len(slices)):
            for i in range(slices[si][0], slices[si][1]):
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
        index_set = self.slices.get_index_set()
        row_slices = self.slices.get_row_slices().get_slices()
        col_slices = self.slices.get_col_slices().get_slices()
        first_row_slice = True
        first_row = True
        for row_slice in row_slices:
            if not first_row_slice:
                yield (-3,-3)
            first_row_slice = False
            for row_i in range(row_slice[0], row_slice[1]):
                if not first_row:
                    yield (-2,-2)
                first_row = False
                first_col = True
                for col_slice in col_slices:
                    if not first_col:
                        yield (row_i,-1)
                    first_col = False
                    for col_i in range(col_slice[0], col_slice[1]):
                        index = (row_i, col_i)
                        if index in index_set:
                            yield index
                        else:
                            yield (row_i,-1)

    def __next__(self):
        return next(self.gen)
