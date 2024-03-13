from Children import Children

def new(children):
    return Children_Key_Value(children) if children else []

class Children_Key_Value(Children):
    
    def __init__(self, data, slicer=None):
        super().__init__(data, slicer)

