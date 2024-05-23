

def slice_elements_recursive(element, sliced_elements, max_tree_depth):
    if max_tree_depth == 0 or element in sliced_elements:
        return
    if element.is_node():
        children = element.get_children()
        if children.is_empty():
            if element.is_node():
                sliced_elements[element] = None
        else:
            slicer = element.get_slicer()
            slices = children.slice(slicer)
            if element.is_node():
                sliced_elements[element] = slices
            if not element.is_hidden_node():
                max_tree_depth -= 1
            for index in slices:
                slice_elements_recursive(children[index], sliced_elements, max_tree_depth)

def slice_elements(element, depth):
    sliced_elements = {}
    slice_elements_recursive(element, sliced_elements, depth)
    return sliced_elements
