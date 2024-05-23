
def print_recursive(element, level, printed_elements): 
    print(' '*level, end='')
    children = element.get_children()
    if children.is_empty():
        print(element.get_data())
    elif element in printed_elements:
        print(f'... ({element})')
    else:
        printed_elements.add(element)
        print(element)
        for index in children.indices_all():
            print_recursive(children[index], level+3, printed_elements)

def print_elements(element):
    print_recursive(element, 0, set())
