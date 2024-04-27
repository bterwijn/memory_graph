
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
        #self.length = length
        self.gen = self.generate()

    def __iter__(self):
        return self

    # def generate(self):
    #     if len(self.slices) > 0:
    #         if self.slices[0][0] > 0:
    #             yield None
    #     for si in range(len(self.slices)):
    #         for i in range(self.slices[si][0], self.slices[si][1]):
    #             yield i
    #         if i < self.length-1:
    #             yield None
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
        for index, slices in self.slices.get_index_slices():
            slices = slices.get_slices()
            for si in range(len(slices)):
                for i in range(slices[si][0], slices[si][1]):
                    yield (index,i)

    def __next__(self):
        return next(self.gen)
