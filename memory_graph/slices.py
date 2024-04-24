import bisect
import copy

from memory_graph.slices_iterator import Slices_Iterator

class Slices:

    def __init__(self, slices=None) -> None:
        self.slices = []
        if not slices is None:
            for i in slices:
                self.add_slice(i)

    def __repr__(self) -> str:
        return f"Slices({self.slices})"
    
    def get_iter(self,length):
        return Slices_Iterator(self.slices,length)

    def copy(self):
        s = Slices()
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

def test_slices():
    test = Slices( [[10,20], [30,40], [60,70], [80,90]] )
    slices = test.copy()
    slices.add_slice([21,79])
    assert slices.get_slices() == [[10,90]], "Slice error: merging begin and end"

    slices = test.copy()
    slices.add_slice([31,39])
    assert slices.get_slices() == [[10,20], [30,40], [60,70], [80,90]], "Slice error: merging begin and end"

    slices = test.copy()
    slices.add_slice([15,50])
    assert slices.get_slices() == [[10,50], [60,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([15,65])
    assert slices.get_slices() == [[10,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([35,45])
    assert slices.get_slices() == [[10,20], [30,45], [60,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([25,65])
    assert slices.get_slices() == [[10,20], [25,70], [80,90]], "Slice error: merging end"
    
    slices = test.copy()
    slices.add_slice([15,65])
    assert slices.get_slices() == [[10,70], [80,90]], "Slice error: merging end"

    slices = test.copy()
    slices.add_slice([55,65])
    assert slices.get_slices() == [[10,20], [30,40], [55,70], [80,90]], "Slice error: merging end"

    slices = test.copy()
    slices.add_slice([25,75])
    assert slices.get_slices() == [[10,20], [25,75], [80,90]], "Slice error: merging none"

    slices = test.copy()
    slices.add_slice([5,6])
    assert slices.get_slices() == [[5,6], [10,20], [30,40], [60,70], [80,90]], "Slice error: merging none"

    slices = test.copy()
    slices.add_slice([95,96])
    assert slices.get_slices() == [[10,20], [30,40], [60,70], [80,90], [95,96]], "Slice error: merging none"

    slices = test.copy()
    assert not slices.add_slice([10,11])
    assert not slices.add_slice([19,20])
    assert not slices.add_slice([30,31])
    assert not slices.add_slice([39,40])
    assert not slices.add_slice([65,66])
    assert slices.add_slice([9,10])
    assert slices.add_slice([20,21])
    assert slices.add_slice([28,29])
    assert slices.add_slice([41,42])
    assert slices.add_slice([75,76])
    assert slices.add_slice([100,200])

if __name__ == "__main__":
    test_slices()
    print("Slices: All tests pass")
