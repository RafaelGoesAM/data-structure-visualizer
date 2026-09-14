from typing import List, Dict, Any, Tuple


class HeapVisualizer:
    """
    Max-Heap implementation designed for visualization.
    Executes algorithmic operations and generates an event trace of all state mutations.
    """

    def __init__(self, initial_data: List[int] = None):
        self.data: List[int] = initial_data[:] if initial_data else []
        self.events: List[Dict[str, Any]] = []

    def _log(self, event_type: str, indices: List[int], description: str) -> None:
        """Appends a snapshot event to the trace execution log."""
        self.events.append({
            "type": event_type,
            "indices": indices,
            "current_state": self.data[:],
            "description": description
        })

    def _swap(self, i: int, j: int, context: str = "") -> None:
        """Swaps two elements in the array and logs a SWAP event."""
        desc = f"Swapped node {self.data[i]} (index {i}) with {self.data[j]} (index {j})"
        if context:
            desc = f"{context}: {desc}"
            
        self.data[i], self.data[j] = self.data[j], self.data[i]
        self._log("SWAP", [i, j], desc)

    # -------------------------------------------------------------------------
    # SIFT OPERATIONS
    # -------------------------------------------------------------------------

    def _sift_up(self, index: int) -> None:
        """Moves a newly inserted element up to its valid heap position."""
        parent = (index - 1) // 2

        while index > 0:
            self._log(
                "COMPARE",
                [index, parent],
                f"Comparing element {self.data[index]} (index {index}) with parent {self.data[parent]} (index {parent})"
            )

            if self.data[index] > self.data[parent]:
                self._swap(index, parent, context="Sifting up")
                index = parent
                parent = (index - 1) // 2
            else:
                break

        self._log(
            "BALANCED",
            [index],
            f"Node {self.data[index]} is now in its correct Heap position"
        )

    def _sift_down(self, index: int, heap_size: int = None) -> None:
        """Restores heap property by pushing a node down to its proper level."""
        if heap_size is None:
            heap_size = len(self.data)

        while True:
            largest = index
            left = 2 * index + 1
            right = 2 * index + 2

            # Evaluate left child
            if left < heap_size:
                self._log(
                    "COMPARE",
                    [index, left],
                    f"Comparing node {self.data[index]} (index {index}) with left child {self.data[left]} (index {left})"
                )
                if self.data[left] > self.data[largest]:
                    largest = left

            # Evaluate right child against current largest candidate
            if right < heap_size:
                self._log(
                    "COMPARE",
                    [largest, right],
                    f"Comparing current max {self.data[largest]} (index {largest}) with right child {self.data[right]} (index {right})"
                )
                if self.data[right] > self.data[largest]:
                    largest = right

            # If a child is larger, swap and continue sifting down
            if largest != index:
                self._swap(index, largest, context="Sifting down")
                index = largest
            else:
                break

        self._log(
            "BALANCED",
            [index],
            f"Subtree rooted at index {index} satisfies the Max-Heap property"
        )

    # -------------------------------------------------------------------------
    # PUBLIC API OPERATIONS
    # -------------------------------------------------------------------------

    def insert(self, value: int) -> Tuple[List[Dict[str, Any]], List[int]]:
        """Appends a new value to the bottom of the heap and sifts it up."""
        self.events.clear()
        self.data.append(value)
        new_index = len(self.data) - 1
        
        self._log(
            "INSERT",
            [new_index],
            f"Inserted new node {value} at index {new_index}"
        )
        
        self._sift_up(new_index)
        return self.events, self.data[:]

    def delete_root(self) -> Tuple[List[Dict[str, Any]], List[int]]:
        """Removes the root (max element), moves last element to root, and sifts down."""
        self.events.clear()

        if not self.data:
            return [], []

        removed_val = self.data[0]
        last_index = len(self.data) - 1

        if len(self.data) == 1:
            self._log("DELETE", [0], f"Removed last remaining root element ({removed_val})")
            self.data.pop()
            return self.events, []

        self._log(
            "DELETE",
            [0, last_index],
            f"Swapping root {removed_val} with last element {self.data[last_index]} for extraction"
        )
        
        self.data[0], self.data[last_index] = self.data[last_index], self.data[0]
        self.data.pop()

        self._log(
            "DELETE",
            [0],
            f"Extracted {removed_val}. Sifting down new root {self.data[0]}"
        )
        
        self._sift_down(0)
        return self.events, self.data[:]

    def build_heap(self, raw_data: List[int]) -> Tuple[List[Dict[str, Any]], List[int]]:
        """Transforms an arbitrary array into a valid Max-Heap in-place."""
        self.events.clear()
        self.data = raw_data[:]
        n = len(self.data)

        self._log(
            "INFO",
            [],
            f"Starting Build-Max-Heap on array of size {n}"
        )

        # Start from the last non-leaf parent node down to root index 0
        start_idx = (n // 2) - 1
        for i in range(start_idx, -1, -1):
            self._log(
                "INFO",
                [i],
                f"Heapifying subtree rooted at index {i} (value: {self.data[i]})"
            )
            self._sift_down(i, heap_size=n)

        self._log(
            "INFO",
            [],
            "Build-Max-Heap complete! Array now satisfies the Max-Heap property."
        )
        return self.events, self.data[:]