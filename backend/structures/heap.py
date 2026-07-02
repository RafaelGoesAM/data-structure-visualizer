class MaxHeap:
    def __init__(self):
        self.heap = []

    def _parent(self, index): return (index - 1) // 2
    def _left_child(self, index): return (2 * index) + 1
    def _right_child(self, index): return (2 * index) + 2

    def insert(self, value):
        """Inserts a value and bubbles it up to preserve Max-Heap invariants."""
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)

    def extract_max(self):
        """Removes and returns the highest value (root), then reheapifies."""
        if len(self.heap) == 0:
            return None
        if len(self.heap) == 1:
            return self.heap.pop()

        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._sift_down(0)
        return root

    def _bubble_up(self, index):
        while index > 0 and self.heap[index] > self.heap[self._parent(index)]:
            parent_idx = self._parent(index)
            self.heap[index], self.heap[parent_idx] = self.heap[parent_idx], self.heap[index]
            index = parent_idx

    def _sift_down(self, index):
        max_index = index
        left = self._left_child(index)
        right = self._right_child(index)

        if left < len(self.heap) and self.heap[left] > self.heap[max_index]:
            max_index = left
        if right < len(self.heap) and self.heap[right] > self.heap[max_index]:
            max_index = right

        if index != max_index:
            self.heap[index], self.heap[max_index] = self.heap[max_index], self.heap[index]
            self._sift_down(max_index)

    def clear(self):
        self.heap.clear()

    def to_dict(self):
        """Returns the array backing the heap representation."""
        return self.heap