from memory_graph.Node import Node

import memory_graph.utils as utils

class Slice:
    """ Represents a slice of data with its starting index. """
    def __init__(self, index, data):
        self.index = index
        self.data = data

    def __len__(self):
        """ Return the length of the data in the slice. """
        return len(self.data)

    def __repr__(self):
        return f"Slice({self.index},{self.data})"

    def transform(self, fun):
        """ Transform the data of the slice using the 'fun' function. """
        self.data = [fun(x) for x in self.data]
        return self
    
    def get_data(self):
        """ Return the data of the slice. """
        return self.data
    

class Sliced_Iterator:
    """ Iterator to iterate through a 'Sliced' object. """

    def __init__(self, slices):
        """ Create a Sliced_Iterator object with the slices of a 'Sliced' object. """
        self.slices = slices
        self.slice_index = 0
        self.value_index = 0
        self.last_index = -1
        self.jump = True if len(self.slices) > 0 and self.slices[0].index > 0 else False

    def __next__(self):
        """ Return the next (index, jump, value) tuple of the 'Sliced' object. Where:
            - 'index' is the index of the value in the data.
            - 'jump' is a boolean indicating if the index is a jump from the previous index.
            - 'value' is the value at the index.
        """
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
    """ Represents data sliced into multiple slices by a Slicer. """

    def __init__(self,length):
        """ Create a Sliced object with the original length of the data. """
        self.original_length = length
        self.slices = []
        
    def __repr__(self):
        return f"Sliced({self.slices})"
    
    def get_original_length(self):
        """ Return the original length of the data."""
        return self.original_length
    
    def add_slice(self, index, data):
        """ Add a slice with the starting index and data to the Sliced object. """
        self.slices.append(Slice(index, data))

    def check_condition_on_children(self, fun):
        """ Check if the condition 'fun' is true for any of the slices. """
        for slice in self.slices:
            if utils.generator_has_data(filter(lambda x: fun(x), slice.data)):
                return True
        return False

    def __iter__(self):
        """ Return a Sliced_Iterator object to iterate through the Sliced object. """
        return Sliced_Iterator(self.slices)
    
    def get_slices(self):
        """ Return the slices of the Sliced object. """
        return self.slices

    def transform(self, fun):
        """ Transform the data of the Sliced object using the 'fun' function. """
        for slice in self.slices:
            slice.transform(fun)
        return self

    def has_data(self):
        """ Return True if the Sliced object has any data. """
        return len(self.slices) > 1 or (len(self.slices) == 1 and len(self.slices[0].data) > 0)
    
    def last_slice_empty(self):
        """ Return True if the last slice of the Sliced object is empty. """
        return len(self.slices) > 0 and len(self.slices[-1].data) == 0
    