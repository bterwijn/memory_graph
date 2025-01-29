# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

from memory_graph.slices import Slices1D
import memory_graph.utils as utils

class Slicer:

    def __init__(self, begin=None, end=None, middle=None, /) -> None:
        self.begin = begin
        self.end = end
        self.middle = middle
        if not self.middle is None:
            self.end, self.middle = self.middle, self.end

    def __repr__(self) -> str:
        return f"Slicer({self.begin},{self.middle},{self.end})"

    def get_slices(self, length):
        slices1d = Slices1D()
        if self.begin is None:
            slices1d.add_slice([0, length])
        else:
            if isinstance(self.begin, float):
                slices1d.add_slice([0, 
                                  min(length,utils.my_round(length*self.begin))]) 
            else:
                slices1d.add_slice([0, 
                                  min(length,self.begin)])
            if not self.middle is None:
                mid = length/2
                if isinstance(self.middle, float):
                    half = length*self.middle/2
                else:
                    half = self.middle/2
                slices1d.add_slice([max(0,utils.my_round(mid-half)), 
                                  min(length,utils.my_round(mid+half))])
            if not self.end is None:
                if isinstance(self.end, float):
                    slices1d.add_slice([max(0,utils.my_round(length-length*self.end)),
                                      length])
                else:
                    slices1d.add_slice([max(0,length-self.end),
                                      length])
        return slices1d
