import memory_graph.extension_numpy as ext_np
import memory_graph.config as config
import torch

config.type_to_node[torch.Tensor] = lambda data : ext_np.ndarray_to_node(data, data.numpy())
config.type_to_color[torch.Tensor] = "darkolivegreen1"
