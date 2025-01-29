# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Extension to add the memory graph configuration for Pandas type. """
from memory_graph.node_linear import Node_Linear
from memory_graph.node_table import Node_Table

import memory_graph.config as config

import pandas as pd

config.type_to_node[pd.DataFrame] = lambda data : (
    Node_Table(data, 
               data.values.tolist(),
               col_names = data.columns.tolist(),
               row_names = [ str(i) for i in data.index.tolist()]
            )
)

config.type_to_node[pd.Series] = lambda data : (
    Node_Linear(data, data.tolist())
)

config.type_to_color[pd.DataFrame] = "olivedrab1"
config.type_to_color[pd.Series] = "olivedrab2"
