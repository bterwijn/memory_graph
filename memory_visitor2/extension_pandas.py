
import pandas as pd
import config
from Node_Linear import Node_Linear
from Node_Table import Node_Table
import config_default
    
config.type_to_node[pd.DataFrame] = lambda data : (
    Node_Table(data, 
               data.values.tolist(),
               column_names=data.columns.tolist(),
               row_names = [ str(i) for i in data.index.tolist()] # TODO: first row problem when 'int' not 'str'
            )
)

config.type_to_node[pd.Series] = lambda data : (
    Node_Linear(data, data.tolist())
)

config.type_to_color[pd.DataFrame] = "olivedrab1"
config.type_to_color[pd.Series] = "olivedrab2"

