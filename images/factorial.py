# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

import memory_graph as mg

image=0
def get_fac_name():
    global image
    image+=1
    return f"factorial{image:02d}.png"

def factorial(n):
    if n==0:
        return 1
    #mg.show( mg.stack(), block=True ) # draw graph
    mg.render( mg.stack(), get_fac_name())
    result = n*factorial(n-1)
    #mg.show( mg.stack(), block=True ) # draw graph
    mg.render( mg.stack(), get_fac_name())
    return result

mg.render( mg.stack(), get_fac_name())
factorial(3)