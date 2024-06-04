import memory_graph
import memory_graph.utils as utils
import memory_graph.config as config

data = utils.nested_list([2,2,2,2,2,2])

config.max_tree_depth = 2
memory_graph.show(data)
