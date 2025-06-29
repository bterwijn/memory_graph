import memory_graph as mg
import random
random.seed(2) # same random numbers each run

class List_View:

    def __init__(self, lst, begin, end):
        self.lst = lst
        self.begin = begin
        self.end = end

    def __getitem__(self, index):
        return self.lst[index]
        
    def get_mid(self):
        return (self.begin + self.end) // 2

def bin_search(view, value):
    mid = view.get_mid()
    if view.begin == mid:
        mg.render(mg.stack(), 'bin_search.png')
        mg.config.type_to_color[List_View] = 'hotpink'
        mg.config.type_to_node[List_View] = lambda data: mg.node_linear.Node_Linear(data,
                                                            data.lst[data.begin:data.end] )
        mg.render(mg.stack(), 'bin_search_linear.png')
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
value = data[random.randrange(n)]
index = bin_search(List_View(data, 0, len(data)), value)
print('index:', index, 'data[index]:', data[index])
