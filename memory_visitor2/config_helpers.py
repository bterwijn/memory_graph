import config

def get_color(node):
    data_id = id(node.get_data())
    if data_id in config.type_to_color:
        return config.type_to_color[data_id]
    data_type = type(node.get_data())
    if data_type in config.type_to_color:
        return config.type_to_color[data_type]
    node_type = type(node)
    if node_type in config.type_to_color:
        return config.type_to_color[node_type]
    return 'white'
    