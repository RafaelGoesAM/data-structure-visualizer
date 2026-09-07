# backend/algorithms/heap.py

from typing import List, Dict, Any, Tuple


class HeapVisualizer:
    """
    Max-Heap implementation designed for visualization.
    Executes algorithmic operations and generates an event trace of all state mutations.
    """

    def __init__(self, initial_data: List[int] = None):
        # Maintain a clean internal state copy
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

            # Max-Heap condition check
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

            # Check left child
            if left < heap_size:
                self._log(
                    "COMPARE",
                    [largest, left],
                    f"Comparing current node {self.data[largest]} (index {largest}) with left child {self.data[left]} (index {left})"
                )
                if self.data[left] > self.data[largest]:
                    largest = left

            # Check right child
            if right < heap_size:
                self._log(
                    "COMPARE",
                    [largest, right],
                    f"Comparing largest node {self.data[largest]} (index {largest}) with right child {self.data[right]} (index {right})"
                )
                if self.data[right] > self.data[largest]:
                    largest = right

            # If a child is larger than the current parent, swap and continue
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
            f"Inserted new node {value} at index {new_index} (bottom of tree)"
        )
        
        self._sift_up(new_index)
        return self.events, self.data[:]

    def delete_root(self) -> Tuple[List[Dict[str, Any]], List[int]]:
        """Removes the root (max element), moves last element to root, and sifts down."""
        self.events.clear()

        if not self.data:
            return [], []

        last_index = len(self.data) - 1
        removed_val = self.data[0]

        if len(self.data) == 1:
            self._log("DELETE", [0], f"Removed last remaining root element ({removed_val})")
            self.data.pop()
            return self.events, []

        self._log(
            "DELETE",
            [0, last_index],
            f"Swapping root {removed_val} with last element {self.data[last_index]} for extraction"
        )
        
        # Swap root with last element and pop it
        self.data[0], self.data[last_index] = self.data[last_index], self.data[0]
        self.data.pop()

        self._log(
            "DELETE",
            [0],
            f"Extracted {removed_val}. Sifting down new root {self.data[0]}"
        )
        
        self._sift_down(0)
        return self.events, self.data[:]

    def heapsort(self) -> Tuple[List[Dict[str, Any]], List[int]]:
        """Transforms array into Max-Heap and performs full Heapsort."""
        self.events.clear()
        n = len(self.data)

        if n <= 1:
            return self.events, self.data[:]

        # Step 1: Build Max-Heap (bottom-up)
        self._log("INFO", [], "Phase 1: Building Max-Heap from unstructured array")
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i, n)

        # Step 2: Extract elements one by one
        self._log("INFO", [], "Phase 2: Extracting maximum element and sorting array")
        for i in range(n - 1, 0, -1):
            # Swap current root (max) to the sorted partition at index i
            self._swap(0, i, context="Extracting Max to sorted array boundary")
            
            self._log(
                "MARK_SORTED",
                [i],
                f"Element {self.data[i]} placed in final sorted position"
            )
            
            # Restore heap property on remaining unsorted partition
            self._sift_down(0, i)

        # Mark index 0 as sorted
        self._log("MARK_SORTED", [0], f"Element {self.data[0]} placed in final sorted position")
        return self.events, self.data[:]