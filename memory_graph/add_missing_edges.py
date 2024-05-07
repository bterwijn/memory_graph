

def add_indices_to_parents(element, sliced_elements_old_keys, sliced_elements):
    parent_indices = element.get_parent_indices()
    for parent, indices in parent_indices.items():
        for index in indices:
            sliced_elements[parent].add_index(index)

def add_missing_edges(sliced_elements):
    sliced_elements_old_keys = list(sliced_elements.keys())
    for element in sliced_elements_old_keys:
        add_indices_to_parents(element, sliced_elements_old_keys, sliced_elements)
    return sliced_elements
