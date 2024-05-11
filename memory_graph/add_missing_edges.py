
def add_parent_indices(type_to_parent_indices, sliced_elements, max_missing_edges):
    #print('add_parent_indices type_to_parent_indices:',type_to_parent_indices)
    for _, parent_indices in type_to_parent_indices.items():
        dashed = len(parent_indices) > max_missing_edges
        for parent, index in parent_indices[0:max_missing_edges]:
            new_parent = False
            if not parent in sliced_elements:
                new_parent = True
                sliced_elements[parent] = parent.get_children().empty_slices()
            slices = sliced_elements[parent]
            slices.add_index(index, dashed=dashed)
            if new_parent:
                add_indices_to_parents(parent, sliced_elements, max_missing_edges)

def add_indices_to_parents(element, sliced_elements, max_missing_edges):
    #print('add_indices_to_parents element:',element)
    type_to_parent_indices = {}
    parent_indices = element.get_parent_indices()
    for parent, indices in parent_indices.items():
        parent_type = parent.get_type()
        if (parent_type in type_to_parent_indices and 
            len(type_to_parent_indices[parent_type]) > max_missing_edges): # early stop
            continue
        parent_slices = None
        if parent in sliced_elements:
            parent_slices = sliced_elements[parent]
        for index in indices:
            if parent_slices is None or not parent_slices.has_index(index):
                if not parent_type in type_to_parent_indices:
                    type_to_parent_indices[parent_type] = []
                parent_indices = type_to_parent_indices[parent_type]
                if len(parent_indices) > max_missing_edges:
                    break
                else:
                    parent_indices.append((parent, index))
    add_parent_indices(type_to_parent_indices, sliced_elements, max_missing_edges)

def add_missing_edges(sliced_elements, max_missing_edges=3):
    old_sliced_elements_keys = set(sliced_elements.keys())
    for element in old_sliced_elements_keys:
        add_indices_to_parents(element, sliced_elements, max_missing_edges)
    return sliced_elements
