
class Node:
    def __init__(self, data):
        self.prev = None
        self.data = data
        self.next = None

class Iterator:
    def __init__(self, node):
        self.current = node
        
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current is None:
            raise StopIteration
        else:
            data = self.current.data
            self.step()
            return data

class Iterator_Forward(Iterator):
    def __init__(self, node):
        super().__init__(node)
        
    def step(self):
        self.current = self.current.next

class Iterator_Backward(Iterator):
    def __init__(self, node):
        super().__init__(node)
        
    def step(self):
        self.current = self.current.prev

class Linked_List:
    def __init__(self):
        self.head = None
        self.tail = None

    def __iter__(self):
        return Iterator_Forward(self.head)

    def __reversed__(self):
        return Iterator_Backward(self.tail)

    def insert_tail(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail.next.prev = self.tail
            self.tail = new_node

print("build a linked list:")
linked_list = Linked_List()
for value in range(5):
    print('insert:', value)
    linked_list.insert_tail(value)

print("forward iterate through the list:")
for value in linked_list:
    print(value)

print("what the for-loop does under the hood:")
iterator = iter(linked_list)  # get iterator
while True:
    try:
        value = next(iterator)  # get next value
        print(value)
    except StopIteration:  # signals end of iteration
        break  # iteration finished

print("backward iterate through the list:")
for value in reversed(linked_list):
    print(value)

print('done')