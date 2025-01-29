# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause


from memory_graph.slices import Slices1D, Slices2D

def test_slices1d():
    test = Slices1D( [[10,20], [30,40], [60,70], [80,90]] )
    slices = test.copy()
    slices.add_slice([21,79])
    assert slices.get_slices() == [[10,90]], "Slice error: merging begin and end"

    slices = test.copy()
    slices.add_slice([31,39])
    assert slices.get_slices() == [[10,20], [30,40], [60,70], [80,90]], "Slice error: merging begin and end"

    slices = test.copy()
    slices.add_slice([15,50])
    assert slices.get_slices() == [[10,50], [60,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([15,65])
    assert slices.get_slices() == [[10,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([35,45])
    assert slices.get_slices() == [[10,20], [30,45], [60,70], [80,90]], "Slice error: merging begin"

    slices = test.copy()
    slices.add_slice([25,65])
    assert slices.get_slices() == [[10,20], [25,70], [80,90]], "Slice error: merging end"
    
    slices = test.copy()
    slices.add_slice([15,65])
    assert slices.get_slices() == [[10,70], [80,90]], "Slice error: merging end"

    slices = test.copy()
    slices.add_slice([55,65])
    assert slices.get_slices() == [[10,20], [30,40], [55,70], [80,90]], "Slice error: merging end"

    slices = test.copy()
    slices.add_slice([25,75])
    assert slices.get_slices() == [[10,20], [25,75], [80,90]], "Slice error: merging none"

    slices = test.copy()
    slices.add_slice([5,6])
    assert slices.get_slices() == [[5,6], [10,20], [30,40], [60,70], [80,90]], "Slice error: merging none"

    slices = test.copy()
    slices.add_slice([95,96])
    assert slices.get_slices() == [[10,20], [30,40], [60,70], [80,90], [95,96]], "Slice error: merging none"

    slices = test.copy()
    assert not slices.add_slice([10,11])
    assert not slices.add_slice([19,20])
    assert not slices.add_slice([30,31])
    assert not slices.add_slice([39,40])
    assert not slices.add_slice([65,66])
    assert slices.add_slice([9,10])
    assert slices.add_slice([20,21])
    assert slices.add_slice([28,29])
    assert slices.add_slice([41,42])
    assert slices.add_slice([75,76])
    assert slices.add_slice([100,200])
    
    test = Slices1D( [ [i,i+2] for i in range(0,30,4)] )
    #print('test:',test)
    for index in range(30):
        #print('index:',index, 'has_index:',test.has_index(index))
        assert test.has_index(index) == ((index//2) % 2 == 0), f"Error: {index}"

def test_slices2d():
    from memory_graph.slices import Slices
    slices2d = Slices2D( Slices1D([[20,30]]),
                         Slices1D([[20,30]])
    )
    
    slices2d.add_index((19,19))
    slices2d.add_index((31,31))
    print(slices2d)
    slices2d.add_index((18,19))
    print(slices2d)
    slices2d.add_index((19,18))
    slices2d.add_index((30,30))
    print(slices2d)

if __name__ == "__main__":
    test_slices1d()
    test_slices2d()
    print("Slices: All tests pass")
