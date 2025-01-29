# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause


class List_View:
    def __init__(self, base_list, begin, end):
        self.base_list = base_list
        self.begin = max(0, begin)
        self.end = min(end, len(base_list))

    def __getitem__(self, index):
        if isinstance(index, slice):
            # Calculate new begin and end indices within the bounds of the current view
            start, stop, step = index.indices(self.end - self.begin)
            if step != 1:
                raise ValueError("List_View does not support slices with steps other than 1")
            # Adjust the indices relative to the base list
            new_start = self.begin + start
            new_end = self.begin + stop
            return List_View(self.base_list, new_start, new_end)
        elif isinstance(index, int):
            if index < 0 or index >= (self.end - self.begin):
                raise IndexError("list index out of range")
            return self.base_list[self.begin + index]
        else:
            raise TypeError("Invalid index type")

    def __setitem__(self, index, value):
        if index < 0 or index >= (self.end - self.begin):
            raise IndexError("list index out of range")
        self.base_list[self.begin + index] = value

    def __len__(self):
        return self.end - self.begin

    def __iter__(self):
        for i in range(self.begin, self.end):
            yield self.base_list[i]

    def __repr__(self):
        return f"List_View({self.base_list[self.begin:self.end]})"

def test_list_vew():
    original_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    list_view = List_View(original_list, 3, 8)
    print(list_view)  # Output: List_View([3, 4, 5, 6, 7])
    print(list_view[1:4])  # Output: List_View([4, 5, 6])
    # 2D array
    n = 4
    data = [i for i in range(n*n)]
    list_views = [List_View(data, i, i+n) for i in range(0,len(data),n)]
    for row in list_views:
        print(row)

if __name__ == "__main__":
    test_list_vew()
