# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph

import memory_graph.test as test

if __name__ == '__main__':
    test_fun_count = 0
    def test_fun(data):
        global test_fun_count
        memory_graph.render(data, f'test_graph{test_fun_count}.png')
        test_fun_count += 1
    test.test_all(test_fun)
