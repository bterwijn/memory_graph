import utils

def make_subgraph(children):
    return '{ rank="same"  '+(" -> ".join(children))+'  [weight=99,style=invis]; }\n'

def make_node_body(category):
    return category.get_body()
