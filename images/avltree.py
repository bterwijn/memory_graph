import memory_graph as mg
import bintrees

# Create an AVL tree
tree = bintrees.AVLTree()
tree.insert(10, "ten")
tree.insert(5, "five")
tree.insert(20, "twenty")
tree.insert(15, "fifteen")

mg.render(locals(), 'avltree_fail.png')

mg.config.type_to_color[bintrees.avltree.Node] = "sandybrown"
mg.render(locals(), 'avltree_color.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_linear.Node_Linear(data, dir(data))
mg.config.type_to_slicer[bintrees.avltree.Node] = mg.slicer.Slicer()
mg.render(locals(), 'avltree_dir.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_base.Node_Base(f"key:{data.key} value:{data.value}")
mg.render(locals(), 'avltree_base.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_linear.Node_Linear(data,
                                                                                        ['left', data.left,
                                                                                         'key', data.key,
                                                                                         'value', data.value,
                                                                                         'right', data.right])
mg.render(locals(), 'avltree_linear.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_key_value.Node_Key_Value(data,
                                                                                              {'left': data.left,
                                                                                               'key': data.key,
                                                                                               'value': data.value,
                                                                                               'right': data.right}.items())
mg.render(locals(), 'avltree_key_value.png')

mg.config.type_to_node[bintrees.avltree.Node] = lambda data: mg.node_table.Node_Table(data,
                                                                                      [[data.key, data.value],
                                                                                       [data.left, data.right]]
                                                                                      )
mg.render(locals(), 'avltree_table.png')
