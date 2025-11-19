
class Node:
    """ Node in a doubly linked list """

    def __init__(self, value, prev=None, next=None):
        self.prev = prev
        self.value = value
        self.next = next

class Linked_List:
    """ Linear Doubly Linked List """

    def __init__(self):
        self.head = None
        self.tail = None

    def add_back(self, value):
        new_node = Node(value, self.tail, None)
        if self.tail is None:
            # Empty list
            self.head = self.tail = new_node
        else:
            # Append to tail
            self.tail.next = new_node
            self.tail = new_node

linked_list = Linked_List()
n = 20
for value in range(n):
    linked_list.add_back(value)
