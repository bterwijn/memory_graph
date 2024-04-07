import memory_graph
import pandas as pd
import memory_graph.extension_pandas

series = pd.Series( [i for i in range(20)] )
dataframe1 = pd.DataFrame({  "calories": [420, 380, 390],
                             "duration": [50, 40, 45] })
dataframe2 = pd.DataFrame({  'Name'   : [ 'Tom', 'Anna', 'Steve', 'Lisa'],
                             'Age'    : [    28,     34,      29,     42],
                             'Length' : [  1.70,   1.66,    1.82,   1.73] },
                            index=['one', 'two', 'three', 'four']) # with row names

memory_graph.render( locals(), "extension_pandas.png")
