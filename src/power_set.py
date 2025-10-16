
def get_subsets(subsets, data, i, subset):
    if i == len(data):
        subsets.append(subset.copy())
        return
    subset.append(data[i])
    get_subsets(subsets, data, i+1, subset)  #    do include data[i]
    subset.pop()
    get_subsets(subsets, data, i+1, subset)  # don't include data[i]

def power_set(data):
    subsets = []
    get_subsets(subsets, data, 0, [])
    return subsets

print( power_set(['a', 'b', 'c']) )
