
def get_key_values(dictionary):
    return [Key_Value(tup) for tup in dictionary.items()]

class Key_Value:

    def __init__(self, tup):
        self.tup = list(tup)

    def __repr__(self):
        return f'Key_Value({self.tup})'

    def do_backtrack_callback(self):
        return False

    def get_tuple(self):
        return self.tup

    def get_children(self):
        return self
    
    def transform(self, fun):
        for i in range(len(self.tup)):
            self.tup[i] = fun(self.tup[i])
        
    def visit_with_depth(self, fun):
        for i in self.tup:
            fun( (0, i) )