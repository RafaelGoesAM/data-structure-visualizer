class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, value):
        """Adds an item to the back of the queue."""
        self.items.append(value)

    def dequeue(self):
        """Removes and returns the item at the front of the queue."""
        if not self.is_empty():
            return self.items.pop(0)
        return None

    def peek(self):
        """Returns the front item without removing it."""
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def clear(self):
        self.items.clear()

    def to_dict(self):
        """Returns the underlying array representing the queue order."""
        return self.items