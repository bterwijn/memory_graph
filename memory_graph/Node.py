
all_nodes=[]

def print_all_nodes(all_nodes):
    for i,n in enumerate(all_nodes):
        print(i,n)
        
class Node:
    index=0
    
    def __init__(self,original_data):
        self.original_data=original_data
        self.index=Node.index
        self.elements=[]
        self.ref=None
        all_nodes.append(self)
        Node.index+=1
        
    def __repr__(self):
        return f"index:{self.index} type:{self.get_type()} elements:{self.elements}"

    def get_original_data(self):
        return self.original_data
        
    def get_type(self):
        return type(self.original_data)
        
    def get_index(self):
        return self.index

    def get_ref(self):
        if self.ref==None:
            self.ref=Element(ref=self.index)
        return self.ref
    
    def get_elements(self):
        return self.elements

    def add_elements(self,elements):
        for e in elements:
            self.add_element(e)
        
    def add_element(self,element):
        self.elements.append(element)

class Element:

    def __init__(self,value=None,ref=None):
        self.value=value
        self.ref=ref

    def __repr__(self):
        s=""
        if not self.value is None:
            s+=f"value:{self.value} "
        if not self.ref is None:
            s+=f"ref:{self.ref} "
        return s

    def set_value(self,value):
        self.value=value

    def get_value(self):
        return self.value

    def set_ref(self,ref):
        self.ref=ref

    def get_ref(self):
        return self.ref
