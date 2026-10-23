# This file is part of memory_graph.
# Copyright (c) 2023, Bas Terwijn.
# SPDX-License-Identifier: BSD-2-Clause

""" Extension to add the memory graph configuration for Polars types. """
from memory_graph.node_table import Node_Table

import memory_graph.config as config
import memory_graph.config_default as config_default

def extend_polars():
    import polars as pl

    #config.type_to_color[pl.DataFrame] = "aquamarine"
    config.type_to_node[pl.DataFrame] = lambda df: Node_Table(df,
                                                            df.iter_rows(),
                                                            col_names = df.columns)
    config_default.type_to_color_light[pl.DataFrame] = "aquamarine"
    config_default.type_to_color_dark[pl.DataFrame] = "#295345"

    if not config.color_mode_dark:
        config.type_to_color[pl.DataFrame] = config_default.type_to_color_light[pl.DataFrame]
    else:
        config.type_to_color[pl.DataFrame] = config_default.type_to_color_dark[pl.DataFrame]

def unextend_polars():
    import polars as pl
    
    del config.type_to_node[pl.DataFrame]
    del config.type_to_color[pl.DataFrame]
