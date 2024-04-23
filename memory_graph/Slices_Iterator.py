class Slices_Iterator:

    def __init__(self, slices):
        self.slices = slices
        self.si = 0
        if self.si < len(slices):
            self.i = slices[0][0]

    def __iter__(self):
        return self

    def __next__(self):
        if self.si >= len(self.slices):
            raise StopIteration
        if self.i >= self.slices[self.si][1]:
            self.si += 1
            jump = True
            if self.si >= len(self.slices):
                raise StopIteration
            self.i = self.slices[self.si][0]
        else:
            jump = False
        value = self.i
        self.i += 1
        return value, jump        

def test_slices_iterator():
    test = Slices( [[10,20], [30,40], [60,70], [80,90]] )
    slices = Slices_Iterator(test.get_slices())
    for i in slices:
        print(i)
    #assert list(slices) == [10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89], "Slices_Iterator error: slices iteration"

if __name__ == '__main__':
    test_slices_iterator()
    print("Slices_Iterator: All tests pass")    