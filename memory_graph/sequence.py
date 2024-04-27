from abc import ABC, abstractmethod

from memory_graph.slices import Slices2D
import memory_graph.utils as utils

class Sequence(ABC):

    @abstractmethod
    def size():
        pass

    @abstractmethod
    def slice(self, slicer):
        pass

    @abstractmethod
    def apply_all(self, fun):
        pass

    @abstractmethod
    def indices_all(self):
        pass

    @abstractmethod
    def __getitem__(self, index):
        pass

    @abstractmethod
    def apply(self, slices, fun):
        pass


class Sequence1D(Sequence):

    def __init__(self, data):
        self.data = utils.make_sliceable(data)

    def __repr__(self):
        return f'Sequence1D: {self.data}'
    
    def size(self):
        return len(self.data)
    
    def slice(self, slicer):
        return slicer.get_slices( len(self.data) )
    
    def apply_all(self, fun):
        for i in self.data:
            fun(i)

    def indices_all(self):
        for i in range(len(self.data)):
            yield i

    def __getitem__(self, index):
        return self.data[index]

    def apply(self, slices, fun):
        for s in slices.get_slices():
            for i in range(s[0], s[1]):
                fun(self.data[i])

class Sequence2D(Sequence):

    def __init__(self, data):
        self.data = utils.make_sliceable(data)

    def __repr__(self):
        return f'Sequence2D: {self.data}'
    
    def size(self):
        l1, l2 = len(self.data), 0
        if l1 > 0:
            l2 = len(self.data[0])
        return l1, l2
    
    def slice(self, slicer0):
        if type(slicer0) is tuple:
            slicer0, slicer1 = slicer0
        else:
            slicer1 = slicer0
        slices0 = slicer0.get_slices( len(self.data) )
        slices1 = slicer1.get_slices( len(self.data[0]) )
        slices2d = Slices2D()
        for s in slices0.get_slices():
            for i in range(s[0], s[1]):
                #print('s:',i, slices1)
                slices2d.add_slices(i, slices1.copy())
                #print('slices2d:',slices2d)
        return slices2d
    
    def apply_all(self, fun):
        for row in self.data:
            for i in row:
                fun(i)

    def indices_all(self):
        len0 = len(self.data) 
        if len0 > 0:
            len1 = len(self.data[0])
            for y in range(len0):
                for x in range(len1):
                    yield (y,x)

    def __getitem__(self, index):
        return self.data[index[0]][index[1]]

    def apply(self, slices, fun):
        for index,slices in slices.get_index_slices():
            for s in slices.get_slices():
                for i in range(s[0], s[1]):
                    fun(self.data[index][i])

