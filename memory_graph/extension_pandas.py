# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Extension to add the memory graph configuration for Pandas types. """
from memory_graph.node_linear import Node_Linear
from memory_graph.node_table import Node_Table

import memory_graph.config as config
import memory_graph.config_default as config_default

def extend_pandas():
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

    config_default.type_to_color_light[pd.DataFrame] = "olivedrab1"
    config_default.type_to_color_light[pd.Series] = "olivedrab2"

    config_default.type_to_color_dark[pd.DataFrame] = "#3a4d13"
    config_default.type_to_color_dark[pd.Series] = "#3a4d13"

    if not config.color_mode_dark:
        config.type_to_color[pd.DataFrame] = config_default.type_to_color_light[pd.DataFrame]
        config.type_to_color[pd.Series] = config_default.type_to_color_light[pd.Series]
    else:
        config.type_to_color[pd.DataFrame] = config_default.type_to_color_dark[pd.DataFrame]
        config.type_to_color[pd.Series] = config_default.type_to_color_dark[pd.Series]


def unextend_pandas():
    import pandas as pd

    del config.type_to_node[pd.DataFrame]
    del config.type_to_node[pd.Series]

    del config.type_to_color[pd.DataFrame]
    del config.type_to_color[pd.Series]
