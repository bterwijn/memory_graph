
def default_backtrack_callback(node):
    print("default callback:", node)

class Memory_Visitor:
    
    def __init__(self, backtrack_callback=None):
        self.backtrack_callback = default_backtrack_callback if backtrack_callback is None else backtrack_callback 
        self.data_ids = set()

    def visit(self, data):
        self.visit_recursive(data, None)

    def visit_recursive(self, data, parent_node):
        #if (parent_node != None and type(data) in no_reference_types):
        #    return node_layout.format_string(data)
        id = id(data)
        if id in self.data_ids:
            return
        else:
            self.data_ids.add(id)
        return node

    def data_to_node(self, data):
        pass
