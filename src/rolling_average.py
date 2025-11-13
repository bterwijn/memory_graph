import random

class Rolling_Average:

    def __init__(self, data, window):
        self.data = data
        self.window = window
        self.index_begin = 0
        self.index_end = 0
        self.total = 0

    def __iter__(self):
        return self

    def _forward_end(self):
        self.total += self.data[self.index_end]
        self.index_end += 1
    
    def _forward_begin(self):
        self.total -= self.data[self.index_begin]
        self.index_begin += 1

    def get_size(self):
        return self.index_end - self.index_begin
    
    def get_average(self):
        if self.get_size() == 0:
            return float("nan")
        return self.total / self.get_size()
    
    def __next__(self):
        if self.index_end < len(self.data):
            self._forward_end()
            if self.get_size() > self.window:
                self._forward_begin()
        else:
            self._forward_begin()
        if self.index_begin >= len(self.data):
            raise StopIteration
        return self.get_average()
        
mg.config.type_to_node[Rolling_Average] = lambda r : mg.Node_Linear(r, 
   [v if r.index_begin <= i < r.index_end else '' for i,v in enumerate(r.data)] + ['__avg__:', r.get_average()]
    if hasattr(r, 'total') else [''])


n = 10
data = [i for i in range(n)]
print(data)
averages = []
rolling_average = Rolling_Average(data, 4)
for a in rolling_average:
    averages.append(a)
print(averages)
