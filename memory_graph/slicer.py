from memory_graph.slices import Slices
import memory_graph.utils as utils

class Slicer:

    def __init__(self, begin=None, end=None, middle=None, /) -> None:
        self.begin = begin
        self.end = end
        self.middle = middle
        if not self.middle is None:
            self.end, self.middle = self.middle, self.end

    def __repr__(self) -> str:
        return f"Slicer({self.begin},{self.middle},{self.end})"

    def get_slices(self, length):
        slices = Slices()
        if self.begin is None:
            slices.add_slice([0, length])
        else:
            if isinstance(self.begin, float):
                slices.add_slice([0, 
                                  min(length,utils.my_round(length*self.begin))]) 
            else:
                slices.add_slice([0, 
                                  min(length,self.begin)])
            if not self.middle is None:
                mid = length/2
                if isinstance(self.middle, float):
                    half = length*self.middle/2
                else:
                    half = self.middle/2
                slices.add_slice([max(0,utils.my_round(mid-half)), 
                                  min(length,utils.my_round(mid+half))])
            if not self.end is None:
                if isinstance(self.end, float):
                    slices.add_slice([max(0,utils.my_round(length-length*self.end)),
                                      length])
                else:
                    slices.add_slice([max(0,length-self.end),
                                      length])
        #print("slices:",slices)
        return slices

def test_slicer():
    slicer = Slicer(0.1, 0.2, 0.3)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [40, 60], [70, 100]], "Slicer error"

    slicer = Slicer(10, 20, 30)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [40, 60], [70, 100]], "Slicer error"

    slicer = Slicer(0.1, 0.3)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [70, 100]], "Slicer error"

    slicer = Slicer(10, 30)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10], [70, 100]], "Slicer error"

    slicer = Slicer(0.1)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10]], "Slicer error"

    slicer = Slicer(10)
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 10]], "Slicer error"

    slicer = Slicer()
    slices = slicer.get_slices(100)
    assert slices.get_slices() == [[0, 100]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(0)
    assert slices.get_slices() == [[0,0]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(5)
    assert slices.get_slices() == [[0,5]], "Slicer error"

    slicer = Slicer(2,2)
    slices = slicer.get_slices(6)
    assert slices.get_slices() == [[0,2],[4,6]], "Slicer error"

if __name__ == '__main__':
    test_slicer()
    print('Slicer test passed')

# from memory_graph.sliced import Sliced

# import memory_graph.utils as utils

# import math

# def make_sliceable(data):
#     """ Helper function to convert data to a sliceable type if it is not already. """
#     try:
#         data[0:0]
#         return data
#     except TypeError:
#         return list(data)

# class Slicer:
#     """ Slicer can show only the beginning, middle, and end part of data so that the graph remains more readable. """

#     def __init__(self, begin=None, end=None, middle=None, *, _placeholder=None):
#         """ Creates a slicer with the number of 'begin', 'middle', and 'end' elements to show. """
#         self.begin = begin
#         self.end = end
#         self.middle = middle
#         if not self.middle is None:
#             self.end, self.middle = self.middle, self.end

#     def __repr__(self):
#         return f"Slicer({self.begin},{self.middle},{self.end})"

#     def get_begin_index(self, length):
#         """ Helper function to get the index of the end of the beginning of the data. """
#         if type(self.begin) is float:
#             return math.ceil(self.begin*length)
#         return self.begin
    
#     def get_middle_low_index(self, length):
#         """ Helper function to get the index of the beginning of the middle of the data. """
#         if type(self.middle) is float:
#             return utils.my_round(length/2 - self.middle*length)
#         return utils.my_round(length/2 - self.middle/2)

#     def get_middle_high_index(self, length):
#         """ Helper function to get the index of the end of the middle of the data. """
#         if type(self.middle) is float:
#             return utils.my_round(length/2 + self.middle*length)
#         return utils.my_round(length/2 + self.middle/2)

#     def get_end_index(self, length):
#         """ Helper function to get the index of the beginning of the end of the data. """
#         if type(self.end) is float:
#             return math.floor(length-self.end*length)
#         return length-self.end

#     def get_slices(self, length):
#         """ Helper function to get the slices given the length and the 'begin', 'middle', and 'end' sizes. """
#         b = self.get_begin_index(length)
#         slices = [ [0,b] ]
#         if self.middle is not None:
#             m_low = self.get_middle_low_index(length)
#             m_high = self.get_middle_high_index(length)
#             if b + 1 >= m_low:
#                 slices[-1] = [0, m_high]
#             else:
#                 slices.append([m_low,m_high])
#         if self.end is None:
#             slices.append([length,None])
#         else:
#             e = self.get_end_index(length)
#             if slices[-1][1] + 1 >= e:
#                 slices[-1][1] = None
#             else:
#                 slices.append([e,None])
#         return slices

#     def slice(self, data):
#         """ Returns the slices of 'data'. """
#         length = len(data)
#         sliced = Sliced(length)
#         if self.begin is None:
#             sliced.add_slice(0, data)
#         else:
#             data = make_sliceable(data)
#             slices = self.get_slices(length)
#             for index, slice in enumerate(slices):
#                 begin = slice[0]
#                 sli = data[begin:slice[1]]
#                 if len(sli) == 0:
#                     if not sliced.last_slice_empty():
#                         sliced.add_slice(begin, [])
#                 else:
#                     sliced.add_slice(begin, sli)
#         return sliced

#     def slice_2d(self, data, data_width):
#         """ Returns the 2d slices of 'data' given 'data_width' as width. """
#         length = math.ceil(len(data) / data_width)
#         sliced = Sliced(length)
#         if self.begin is None:
#             sliced.add_slice(0, [data[i*data_width:(i+1)*data_width] for i in range(length)] )
#         else:
#             slices = self.get_slices(length)
#             #print('------- slices:',slices)
#             for index, slice in enumerate(slices):
#                 #print('slice:',slice)
#                 begin = slice[0]
#                 end = slice[1] if slice[1] is not None else length
#                 steps = end - begin
#                 d = [data[(begin+s)*data_width:(begin+s+1)*data_width] for s in range(steps)]
#                 #print('d:',d)
#                 if len(d) == 0:
#                     if not sliced.last_slice_empty():
#                         sliced.add_slice(begin, [])
#                 else:
#                     sliced.add_slice(begin, d)
#         return sliced


# def slice_test_size(sliced, sizes):
#     #print('sliced:',sliced)
#     i = 0
#     for slice in sliced.get_slices():
#         # print('slice:',slice,'len:',sizes)
#         assert( len(slice) == sizes[i] )
#         i += 1
#     assert(i == len(sizes))

# def slice_test():
#     print('=== slice_test ===')
#     n = 12
#     data = [i for i in range(n)]
#     slice_test_size(Slicer().slice(data), [12])
#     slice_test_size(Slicer(0).slice(data), [0])
#     slice_test_size(Slicer(2).slice(data), [2,0])
#     slice_test_size(Slicer(0,0).slice(data), [0])
#     slice_test_size(Slicer(0,2).slice(data), [0,2])
#     slice_test_size(Slicer(2,0).slice(data), [2,0])
#     slice_test_size(Slicer(2,2).slice(data), [2,2])
#     slice_test_size(Slicer(0,0,0).slice(data), [0])
#     slice_test_size(Slicer(0,0,2).slice(data), [0,2])
#     slice_test_size(Slicer(0,2,0).slice(data), [0,2,0])
#     slice_test_size(Slicer(0,2,2).slice(data), [0,2,2])
#     slice_test_size(Slicer(2,0,0).slice(data), [2,0])
#     slice_test_size(Slicer(2,0,2).slice(data), [2,0,2])
#     slice_test_size(Slicer(2,2,0).slice(data), [2,2,0])
#     slice_test_size(Slicer(2,2,2).slice(data), [2,2,2])

# def slice_2d_test():
#     print('=== slice_2d_test ===')
#     n = 12
#     k = 5
#     data = [i for i in range(n*k)]
#     slice_test_size(Slicer().slice_2d(data,k), [12])
#     slice_test_size(Slicer(0).slice_2d(data,k), [0])
#     slice_test_size(Slicer(2).slice_2d(data,k), [2,0])
#     slice_test_size(Slicer(0,0).slice_2d(data,k), [0])
#     slice_test_size(Slicer(0,2).slice_2d(data,k), [0,2])
#     slice_test_size(Slicer(2,0).slice_2d(data,k), [2,0])
#     slice_test_size(Slicer(2,2).slice_2d(data,k), [2,2])
#     slice_test_size(Slicer(0,0,0).slice_2d(data,k), [0])
#     slice_test_size(Slicer(0,0,2).slice_2d(data,k), [0,2])
#     slice_test_size(Slicer(0,2,0).slice_2d(data,k), [0,2,0])
#     slice_test_size(Slicer(0,2,2).slice_2d(data,k), [0,2,2])
#     slice_test_size(Slicer(2,0,0).slice_2d(data,k), [2,0])
#     slice_test_size(Slicer(2,0,2).slice_2d(data,k), [2,0,2])
#     slice_test_size(Slicer(2,2,0).slice_2d(data,k), [2,2,0])
#     slice_test_size(Slicer(2,2,2).slice_2d(data,k), [2,2,2])

# if __name__ == '__main__':
#     slice_test()
#     slice_2d_test()