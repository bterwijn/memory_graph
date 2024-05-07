""" Extension to add the memory graph configuration for Pandas type. """
from memory_graph.element_linear import Element_Linear
from memory_graph.element_table import Element_Table

import memory_graph.config as config

import pandas as pd

config.type_to_element[pd.DataFrame] = lambda data : (
    Element_Table(data, 
               data.values.tolist(),
               col_names = data.columns.tolist(),
               row_names = [ str(i) for i in data.index.tolist()]
            )
)

config.type_to_element[pd.Series] = lambda data : (
    Element_Linear(data, data.tolist())
)

config.type_to_color[pd.DataFrame] = "olivedrab1"
config.type_to_color[pd.Series] = "olivedrab2"
