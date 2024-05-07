

def add_indices_to_parents(element, sliced_elements):
    element.get_parents()
    pass

def add_missing_edges(sliced_elements):
    old_sliced_elements = sliced_elements.copy()
    for element, slices in old_sliced_elements.items():
        add_indices_to_parents(element, sliced_elements)
