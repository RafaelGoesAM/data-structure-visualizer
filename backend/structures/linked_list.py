class LinkedListNode:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def insert(self, value):
        """Inserts a new node at the end of the list."""
        new_node = LinkedListNode(value)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def delete(self, value):
        """Deletes the first occurrence of a value."""
        if not self.head:
            return
        
        if self.head.value == value:
            self.head = self.head.next
            return
            
        current = self.head
        while current.next and current.next.value != value:
            current = current.next
            
        if current.next:
            current.next = current.next.next

    def clear(self):
        """Resets the linked list."""
        self.head = None

    def to_dict(self):
        """Serializes the list into an ordered array of node objects for frontend rendering."""
        nodes = []
        current = self.head
        while current:
            nodes.append({
                "value": current.value,
                "has_next": current.next is not None
            })
            current = current.next
        return nodes