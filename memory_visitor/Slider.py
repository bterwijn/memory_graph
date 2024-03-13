
def to_number(s):
    try:
        return int(s)
    except Exception:
        try:
            return float(s)
        except Exception:
            return None

def limit_value(value,size):
    return max(min(value,size-1),-size) 

class Slicer:

    def __init__(self, slices):
        self.slices = []
        for slice in slices:
            s = slice.split(':')
            start = stop = step = None
            if len(s) >= 1:
                start = s[0]
            if len(s) >= 2:
                stop = s[1]
            if len(s) >= 3:
                step = s[2]
            if len(s) > 3:
                raise ValueError(f"Invalid slice: {slice}")
            self.slices.append((to_number(start),to_number(stop),to_number(step)))

    def get_slices(self, size):
        for s in self.slices:
            values = [None if v is None else 
                      limit_value(int(v*size) if isinstance(v,float) else v, size)
                      for v in s]
            yield slice(*values)

    def get_values(self,data):
        for slice in self.get_slices(len(data)):
            print(slice)
            yield data[slice]

if __name__ == '__main__':
    slicer = Slicer([":0.5:2","-0.7::3", "1.5:1.5:1.5", "-1.5:-1.5:-1.5"])
    data = list(range(20))
    for values in slicer.get_values(data):
        print(values)