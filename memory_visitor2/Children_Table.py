from Children import Children

def new(children):
    return Children_Table(children) if children else []

class Children_Table(Children):
    
    def __init__(self, data, slicer=None):
        super().__init__(data, slicer)

