"""
stack.py
--------
A hand-written LIFO STACK (linked-list based) used exclusively by the
Depth First Search algorithm.

Push and Pop are both O(1) since we only ever touch the top pointer.
"""


class _StackNode:
    __slots__ = ("data", "next")

    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """A simple LIFO stack built on a singly linked list."""

    def __init__(self):
        self._top = None
        self._size = 0

    def is_empty(self):
        return self._size == 0

    def push(self, item):
        """Push `item` onto the top of the stack. O(1)."""
        node = _StackNode(item)
        node.next = self._top
        self._top = node
        self._size += 1

    def pop(self):
        """Remove and return the item on top of the stack. O(1)."""
        if self.is_empty():
            raise IndexError("pop from an empty stack")
        node = self._top
        self._top = node.next
        self._size -= 1
        return node.data

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from an empty stack")
        return self._top.data

    def __len__(self):
        return self._size
