
class Slices_Iterator:

    def __init__(self, slices, length):
        self.slices = slices
        self.length = length
        self.gen = self.generate()

    def __iter__(self):
        return self

    def generate(self):
        if len(self.slices) > 0:
            if self.slices[0][0] > 0:
                yield None
        for si in range(len(self.slices)):
            for i in range(self.slices[si][0], self.slices[si][1]):
                yield i
            if i < self.length-1:
                yield None

    def __next__(self):
        return next(self.gen)

def test_slices_iterator():
    from memory_graph.slices import Slices
    test = Slices( [[10,20], [30,40], [60,70], [80,90]] )
    slices = Slices_Iterator(test.get_slices(), 100)
    for i in slices:
        print(i)
    assert list(Slices_Iterator(test.get_slices(), 100)) == [None, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, None, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, None, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, None, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, None], "Slices_Iterator: Error in iteration"

if __name__ == '__main__':
    test_slices_iterator()
    print("Slices_Iterator: All tests pass")    