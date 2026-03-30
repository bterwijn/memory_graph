# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Extension to add the memory graph configuration for Pandas types. """
import memory_graph.extension_numpy as ext_np
import memory_graph.config as config

def extend_torch():
    import torch

    config.type_to_node[torch.Tensor] = lambda data : ext_np.ndarray_to_node(data, data.numpy())
    config.type_to_color[torch.Tensor] = "darkolivegreen1"

def unextend_torch():
    import torch
    
    del config.type_to_node[torch.Tensor]
    del config.type_to_color[torch.Tensor]
