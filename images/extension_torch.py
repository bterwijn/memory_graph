import memory_graph as mg
import torch
import memory_graph.extension_torch
torch.manual_seed(0) # same random numbers each run

tensor_1d = torch.rand(3)
tensor_2d = torch.rand(3, 2)
tensor_3d = torch.rand(2, 2, 2)

mg.render(locals(), 'extension_torch.png')
