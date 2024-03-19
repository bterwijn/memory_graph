import math
import utils 
from Sliced import Sliced

def convert_to_list(data):
    if type(data) is list:
        return data
    return list(data)

def empty_list(list_depth):
    data = []
    for _ in range(list_depth-1):
        data = [data]
    return data

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

    def slice(self, data, list_depth=1):
        data = convert_to_list(data)
        if self.begin is None:
            return [data]
        length = len(data)
        b = self.get_begin_index(length)
        slices = [ [0,b] ]
        if self.middle is not None:
            m_low = self.get_middle_low_index(length)
            m_high = self.get_middle_high_index(length)
            if b + 1 >= m_low:
                slices[-1] = [0, m_high]
            else:
                slices.append([m_low,m_high])
        if self.end is not None:
            e = self.get_end_index(length)
            if slices[-1][1] + 1 >= e:
                slices[-1][1] = None
            else:
                slices.append([e,None])
        sliced = Sliced()
        for index, slice in enumerate(slices):
            s0 = slice[0]
            sli = data[s0:slice[1]]
            if len(sli) == 0:
                if index == len(slices)-1:
                    sliced.add_slice(s0, empty_list(list_depth))
            else:
                sliced.add_slice(s0, sli)
        return sliced
        
if __name__ == '__main__':
    n = 12
    data = [i for i in range(n)]
    print('data:',data)
    slicer = Slicer(0,2,0)
    print('slicer:',slicer)
    sliced = slicer.slice(data)
    print( sliced )
    for v in sliced:
        print(v)
