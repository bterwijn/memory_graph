# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Extension to add the memory graph configuration for Pandas types. """
import memory_graph.extension_numpy as ext_np
import memory_graph.config as config
import memory_graph.config_default as config_default

def extend_torch():
    import torch

    config.type_to_node[torch.Tensor] = lambda data : ext_np.ndarray_to_node(data, data.numpy())

    config_default.type_to_color_light[torch.Tensor] = "darkolivegreen1"

    config_default.type_to_color_dark[torch.Tensor] = "darkolivegreen"

    if not config.color_mode_dark:
        config.type_to_color[torch.Tensor] = config_default.type_to_color_light[torch.Tensor]
    else:
        config.type_to_color[torch.Tensor] = config_default.type_to_color_dark[torch.Tensor]

def unextend_torch():
    import torch
    
    del config.type_to_node[torch.Tensor]
    del config.type_to_color[torch.Tensor]
