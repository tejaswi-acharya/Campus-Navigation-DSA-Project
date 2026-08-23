"""
queue_ds.py
-----------
A hand-written FIFO QUEUE (linked-list based) used exclusively by the
Breadth First Search algorithm.

Why implement it manually?
    This project's purpose is to demonstrate the data structure itself,
    not to lean on Python's `collections.deque`. Enqueue/Dequeue are
    O(1) because we keep both head and tail pointers.
"""


class _QueueNode:
    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    """A simple FIFO queue built on a singly linked list."""

    def __init__(self):
        self._front = None
        self._rear = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def enqueue(self, item):
        """Add `item` to the rear of the queue. O(1)."""
        node = _QueueNode(item)
        if self._rear is None:
            self._front = self._rear = node
        else:
            self._rear.next = node
            self._rear = node
        self._size += 1

    def dequeue(self):
        """Remove and return the item at the front of the queue. O(1)."""
        if self.is_empty():
            raise IndexError("dequeue from an empty queue")
        node = self._front
        self._front = node.next
        if self._front is None:
            self._rear = None
        self._size -= 1
        return node.data

    def __len__(self):
        return self._size
