""" Extension to add the memory graph configuration for Pandas type. """
from memory_graph.Node_Linear import Node_Linear
from memory_graph.Node_Table import Node_Table

import memory_graph.config as config

import pandas as pd

config.type_to_node[pd.DataFrame] = lambda data : (
    Node_Table(data, 
               data.values.tolist(),
               column_names=data.columns.tolist(),
               row_names = [ str(i) for i in data.index.tolist()]
            )
)

config.type_to_node[pd.Series] = lambda data : (
    Node_Linear(data, data.tolist())
)

config.type_to_color[pd.DataFrame] = "olivedrab1"
config.type_to_color[pd.Series] = "olivedrab2"
