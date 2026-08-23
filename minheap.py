"""
minheap.py
----------
A hand-written BINARY MIN-HEAP, used as the priority queue that drives
Dijkstra's algorithm.

Each entry stored in the heap is a tuple: (priority, vertex_name)
The heap is array-based (a plain Python list is used purely as
contiguous storage -- NOT as a "library data structure"; all heap
mechanics: sift-up, sift-down, parent/child index math, are implemented
manually below).

Supported operations:
    push(priority, item)      O(log n)
    pop_min()                 O(log n)  -> returns (priority, item)
    decrease_priority(item,p) O(n) search + O(log n) sift  (lazy variant
                               also supported via re-push, see algorithms.py)
    is_empty()                O(1)
"""


class MinHeap:
    def __init__(self):
        self._data = []   # list of [priority, item] pairs (array-backed tree)

    # ------------------------------------------------------------------
    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    # ------------------------------------------------------------------
    @staticmethod
    def _parent(i):
        return (i - 1) // 2

    @staticmethod
    def _left(i):
        return 2 * i + 1

    @staticmethod
    def _right(i):
        return 2 * i + 2

    # ------------------------------------------------------------------
    def _swap(self, i, j):
        self._data[i], self._data[j] = self._data[j], self._data[i]

    # ------------------------------------------------------------------
    def push(self, priority, item):
        """Insert (priority, item) and sift it up to restore heap order."""
        self._data.append([priority, item])
        self._sift_up(len(self._data) - 1)

    def _sift_up(self, i):
        while i > 0:
            parent = self._parent(i)
            if self._data[i][0] < self._data[parent][0]:
                self._swap(i, parent)
                i = parent
            else:
                break

    # ------------------------------------------------------------------
    def pop_min(self):
        """Remove and return the (priority, item) pair with smallest priority."""
        if self.is_empty():
            raise IndexError("pop_min from an empty heap")
        root = self._data[0]
        last = self._data.pop()
        if self._data:
            self._data[0] = last
            self._sift_down(0)
        return tuple(root)

    def _sift_down(self, i):
        n = len(self._data)
        while True:
            left, right = self._left(i), self._right(i)
            smallest = i
            if left < n and self._data[left][0] < self._data[smallest][0]:
                smallest = left
            if right < n and self._data[right][0] < self._data[smallest][0]:
                smallest = right
            if smallest == i:
                break
            self._swap(i, smallest)
            i = smallest

    # ------------------------------------------------------------------
    def __repr__(self):
        return f"MinHeap({self._data})"
