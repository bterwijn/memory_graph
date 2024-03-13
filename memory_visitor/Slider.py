
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

def list_depth(data):
    depth = 0
    while isinstance(data,list):
        depth += 1
        if len(data) == 0:
            break
        data = data[0]
    return depth

def empty_list(depth):
    data = []
    for _ in range(depth-1):
        data = [data]
    return data

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
            if values[2] == 0:
                values[2] = 1
            yield slice(*values)

    def get_values(self,data):
        if len(data) == 0:
            return data
        depth = list_depth(data)
        first = True
        last_slice = None
        for slice in self.get_slices(len(data)):
            print(slice)
            if first:
                first=False
                if not (slice.start is None or slice.start==0):
                    yield empty_list(depth)
            yield data[slice]
            last_slice = slice
        if not last_slice is None and not (last_slice.stop is None):
            yield empty_list(depth)

if __name__ == '__main__':

    data = [[[[]]]]
    print(empty_list(list_depth(data)))

    slicer = Slicer(["1:0.5:2", "-0.7:-1:"])
    n = 8
    m = 3
    data = [[i*10+j for j in range(m)] for i in range(n)]        
    #data = [list(range(0,5)), list(range(5,10)), list(range(10,15))]
    print('data:',data)
    print(list(slicer.get_values(data)))
    #for values in slicer.get_values(data):
    #    print(values)
