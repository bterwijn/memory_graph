import utils
from Node import Node

class Slice:

    def __init__(self, index, data):
        self.index = index
        self.data = data

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return f"Slice({self.index},{self.data})"

    def transform(self, fun):
        self.data = [fun(x) for x in self.data]
        return self
    
    def get_data(self):
        return self.data
    

class Sliced_Iterator:

    def __init__(self, slices):
        self.slices = slices
        self.slice_index = 0
        self.value_index = 0
        self.last_index = -1
        self.jump = True if len(self.slices) > 0 and self.slices[0].index > 0 else False

    def __next__(self):
        while True:
            if self.slice_index >= len(self.slices):
                raise StopIteration
            current_slice = self.slices[self.slice_index]
            index = current_slice.index + self.value_index
            if len(current_slice.data) == 0:
                self.slice_index += 1
                return (index, True, None)
            elif self.value_index < len(current_slice.data):
                value = current_slice.data[self.value_index]
                self.value_index += 1
                jump = self.jump
                self.jump = False
                return (index, jump, value)
            else:
                self.value_index = 0
                self.slice_index += 1
                self.jump = True

class Sliced:

    def __init__(self,length):
        self.original_length = length
        self.slices = []
        
    def __repr__(self):
        return f"Sliced({self.slices})"
    
    def get_original_length(self):
        return self.original_length
    
    def add_slice(self, index, data):
        self.slices.append(Slice(index, data))

    def check_condition_on_children(self, fun):
        for slice in self.slices:
            if utils.generator_has_data(filter(lambda x: fun(x), slice.data)):
                return True
        return False

    def __iter__(self):
        return Sliced_Iterator(self.slices)
    
    def get_slices(self):
        return self.slices

    def transform(self, fun):
        for slice in self.slices:
            slice.transform(fun)
        return self

    def has_data(self):
        return len(self.slices) > 1 or (len(self.slices) == 1 and len(self.slices[0].data) > 0)
    
    def last_slice_empty(self):
        return len(self.slices) > 0 and len(self.slices[-1].data) == 0