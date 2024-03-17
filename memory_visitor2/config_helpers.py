import config

type_to_color = config.type_to_color
type_to_orientation = config.type_to_orientation
type_to_slicer = config.type_to_slicer

def set_config(colors, orientations, slicers):
    global type_to_color
    global type_to_orientation
    global type_to_slicer
    if colors:
        type_to_color       = config.type_to_color       | colors
    if orientations:
        type_to_orientation = config.type_to_orientation | orientations
    if slicers:
        type_to_slicer      = config.type_to_slicer      | slicers


def get_color(node):
    data_id = id(node.get_data())
    if data_id in type_to_color:
        return type_to_color[data_id]
    data_type = type(node.get_data())
    if data_type in type_to_color:
        return type_to_color[data_type]
    node_type = type(node)
    if node_type in type_to_color:
        return type_to_color[node_type]
    return 'white'
    