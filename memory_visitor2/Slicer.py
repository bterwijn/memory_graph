import math
import utils 
from Sliced import Sliced

def convert_to_list(data):
    if type(data) is list:
        return data
    return list(data)

class Slicer:

    def __init__(self, begin=None, end=None, middle=None, *, _placeholder=None):
        self.begin = begin
        self.end = end
        self.middle = middle
        if not self.middle is None:
            self.end, self.middle = self.middle, self.end

    def __repr__(self):
        return f"Slicer({self.begin},{self.middle},{self.end})"

    def get_begin_index(self, length):
        if type(self.begin) is float:
            return math.ceil(self.begin*length)
        return self.begin
    
    def get_middle_low_index(self, length):
        if type(self.middle) is float:
            return utils.my_round(length/2 - self.middle*length)
        return utils.my_round(length/2 - self.middle/2)

    def get_middle_high_index(self, length):
        if type(self.middle) is float:
            return utils.my_round(length/2 + self.middle*length)
        return utils.my_round(length/2 + self.middle/2)

    def get_end_index(self, length):
        if type(self.end) is float:
            return math.floor(length-self.end*length)
        return length-self.end

    def get_slices(self, length):
        b = self.get_begin_index(length)
        slices = [ [0,b] ]
        if self.middle is not None:
            m_low = self.get_middle_low_index(length)
            m_high = self.get_middle_high_index(length)
            if b + 1 >= m_low:
                slices[-1] = [0, m_high]
            else:
                slices.append([m_low,m_high])
        if self.end is None:
            slices.append([length,None])
        else:
            e = self.get_end_index(length)
            if slices[-1][1] + 1 >= e:
                slices[-1][1] = None
            else:
                slices.append([e,None])
        return slices

    def slice(self, data):
        sliced = Sliced()
        data = convert_to_list(data) # TODO: no list conversion if not sliced?
        if self.begin is None:
            sliced.add_slice(0, data)
        else:
            slices = self.get_slices(len(data))
            print('slices:',slices)
            for index, slice in enumerate(slices):
                start = slice[0]
                sli = data[start:slice[1]]
                if len(sli) == 0:
                    if index == len(slices)-1:
                        sliced.add_slice(start, [])
                else:
                    sliced.add_slice(start, sli)
        return sliced
        
    def slice_2d(self, data, data_width):
        sliced = Sliced()
        length = math.ceil(len(data) / data_width)
        slices = self.get_slices(length)
        for index, slice in enumerate(slices):
            begin = slice[0]
            end = slice[1] if slice[1] is not None else length
            steps = end - begin
            d = [data[(begin+s)*data_width:(begin+s+1)*data_width] for s in range(steps)]
            if index == len(slices)-1:
                d[-1] += [''] * (data_width - len(d[-1]))
            sliced.add_slice(begin, d)
        return sliced

def slice_test():
    print('=== slice_test ===')
    n = 12
    data = [i for i in range(n)]
    print('data:',data)
    slicer = Slicer(0,2,0)
    print('slicer:',slicer)
    sliced = slicer.slice(data)
    print( sliced )
    for v in sliced:
        print(v)

def slice_2d_test():
    print('=== slice_2d_test ===')
    n = 10
    k = 5
    data = [i for i in range(n*k-3)]
    print('data:',data)
    slicer = Slicer()
    print('slicer:',slicer)
    sliced = slicer.slice_2d(data, k)
    print( sliced )
    for v in sliced:
        print(v)

if __name__ == '__main__':
    slice_test()
    slice_2d_test()