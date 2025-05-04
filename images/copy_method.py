# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg
import copy

class My_Class:

    def __init__(self):
        self.digits = [1, 2]
        self.letters = ['x', 'y']

    def custom_copy(self):
        """ Copies 'digits' but shares 'letters'. """
        c = copy.copy(self)
        c.digits = copy.copy(self.digits)
        return c

a = My_Class()
b = a.custom_copy()

mg.render(locals(), 'copy_method.png')
