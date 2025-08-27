
class Linked_List:
    """ Circular Doubly Linked List """

    def __init__(self, value=None, prev=None, next=None):
        self.prev = prev if prev else self
        self.value = value
        self.next = next if next else self

    def add_back(self, value):
        if self.value == None:
            self.value = value 
        else:
            new_node = Linked_List(value, self.prev, self)
            self.prev.next = new_node
            self.prev = new_node

linked_list = Linked_List()
n = 20
for value in range(n):
    linked_list.add_back(value)
