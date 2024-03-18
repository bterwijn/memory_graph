
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

#config.type_to_node[np.ndarray] = ndarray_to_node

#config.type_to_color[np.ndarray] = "hotpink1"
#config.type_to_color[np.matrix] = "hotpink2"


# data = {'Name'   : [ 'Tom', 'Anna', 'Steve', 'Lisa'],
#         'Age'    : [    28,     34,      29,     42],
#         'Length' : [  1.70,   1.66,    1.82,   1.73] }
# dataframe = pd.DataFrame(data)
# print( dataframe)

# row_names = dataframe.index.tolist()
# col_name = dataframe.columns.tolist()
# values = dataframe.values.tolist()

# print('row names:', row_names, type(row_names))
# print('col names:', col_name, type(col_name))
# print('values:', values, type(values))
