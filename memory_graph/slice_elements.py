

def slice_elements_recursive(element, sliced_elements):
    if element in sliced_elements:
        return
    children = element.get_children()
    if children.is_empty():
        if element.is_node():
            sliced_elements[element] = None
    else:
        slicer = element.get_slicer()
        slices = children.slice(slicer)
        if element.is_node():
            sliced_elements[element] = slices
        for index in children.indices_all():
            slice_elements_recursive(children[index], sliced_elements)

def slice_elements(element):
    element_to_slices = {}
    slice_elements_recursive(element, element_to_slices)
    return element_to_slices
