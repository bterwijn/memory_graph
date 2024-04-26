import bisect
from memory_graph.slices import Slices

class Slices2D:

    def __init__(self):
        self.index_slices = []

    def __repr__(self):
        s=''
        for i in self.index_slices:
            s += str(i) + '\n'
        return s
    
    def get_index_slices(self):
        return self.index_slices

    def add_slice(self, index, slices, remove_interposed_dots=1):
        insert = bisect.bisect_left(self.index_slices, index, key=lambda x: x[0])
        if insert < len(self.index_slices):
            if self.index_slices[insert][0] == index:
                slices_update = self.index_slices[insert][1]
                for s in slices.get_slices():
                    slices_update.add_slice(s, remove_interposed_dots)
                return
        self.index_slices.insert(insert, [index, slices])

def test_Slices2D():
    slices2d = Slices2D()
    slices2d.add_slice(2, Slices([[0,10], [20,30]]))
    slices2d.add_slice(0, Slices([[0,10], [20,30]]))
    slices2d.add_slice(1, Slices([[0,10], [20,30]]))
    slices2d.add_slice(1, Slices([[5,22]]))
    slices2d.add_slice(1, Slices([[30,31]]))
    slices2d.add_slice(0, Slices([[11,13]]))
    slices2d.add_slice(0, Slices([[18,19]]),0)
    print(slices2d)
    slices2d.add_slice(0, Slices([[19,20]]),0)
    print(slices2d)

if __name__ == '__main__':
    test_Slices2D()
