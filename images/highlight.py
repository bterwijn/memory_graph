import memory_graph
from memory_graph.slicer import Slicer

data = [ list(range(20)) for i in range(1,5)]
highlight = data[2]

memory_graph.render( locals(), "highlight.png",
    colors                = {id(highlight): "red"   }, # set color to "red"
    vertical_orientations = {id(highlight): False   }, # set horizontal orientation
    slicers               = {id(highlight): Slicer()}  # set no slicing 
)
