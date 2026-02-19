import random

class List_View:

    def __init__(self, lst, begin, end):
        self.lst = lst
        self.begin = begin
        self.end = end

    def __getitem__(self, index):
        return self.lst[index]

    def get_mid(self):
        return (self.begin + self.end) // 2

# Show List_View as sublist
mg.config.type_to_node[List_View] = (lambda l: mg.Node_Linear(l,
    [v if l.begin <= i < l.end else '' for i, v in enumerate(l.lst)]
    if hasattr(l, 'end') else [])
)
    
def bin_search(view, value):
    mid = view.get_mid()
    if view.begin == mid:
        return view.begin
    if value < view[mid]:
        return bin_search(List_View(view.lst, view.begin, mid), value)
    else:
        return bin_search(List_View(view.lst, mid, view.end), value)

# create sorted list
n = 15
data = [random.randrange(1000) for _ in range(n)]
data.sort()

# search 'value'
value = data[random.randrange(len(data))]
index = bin_search(List_View(data, 0, len(data)), value)
print('found at index:', index, 'data[index]:', data[index])
