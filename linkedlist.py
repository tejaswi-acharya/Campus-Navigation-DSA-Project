"""
linkedlist.py
-------------
A hand-written SINGLY LINKED LIST used as the underlying storage for each
vertex's adjacency list inside the Graph class.

Why a linked list instead of a Python list for adjacency?
    This is a Data Structures course project -- the whole point is to show
    that we understand how an adjacency list is actually built from first
    principles (node -> node -> node -> None), not just call `list.append`.

Each node in the linked list represents ONE edge leaving a vertex:
    neighbour name + edge weight.

Example (conceptually):

    Library -> DoEC(56) -> Canteen(50) -> None
"""


class AdjacencyNode:
    """A single node in the adjacency linked list. Represents one edge."""

    __slots__ = ("neighbour", "weight", "next")

    def __init__(self, neighbour, weight):
        self.neighbour = neighbour   # name of the connected vertex
        self.weight = weight         # edge weight (distance in meters)
        self.next = None             # pointer to the next AdjacencyNode


class LinkedList:
    """
    A minimal singly linked list supporting the operations the Graph
    class needs: append (insert edge), search, remove, and iteration.
    """

    def __init__(self):
        self.head = None
        self._size = 0

    # ------------------------------------------------------------------
    def append(self, neighbour, weight):
        """Insert a new edge (neighbour, weight) at the END of the list."""
        new_node = AdjacencyNode(neighbour, weight)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    # ------------------------------------------------------------------
    def remove(self, neighbour):
        """Remove the edge pointing to `neighbour`, if it exists."""
        prev = None
        current = self.head
        while current is not None:
            if current.neighbour == neighbour:
                if prev is None:
                    self.head = current.next
                else:
                    prev.next = current.next
                self._size -= 1
                return True
            prev = current
            current = current.next
        return False

    # ------------------------------------------------------------------
    def get_weight(self, neighbour):
        """Return the weight of the edge to `neighbour`, or None."""
        current = self.head
        while current is not None:
            if current.neighbour == neighbour:
                return current.weight
            current = current.next
        return None

    # ------------------------------------------------------------------
    def __iter__(self):
        """Allow `for neighbour, weight in linked_list:` iteration."""
        current = self.head
        while current is not None:
            yield current.neighbour, current.weight
            current = current.next

    # ------------------------------------------------------------------
    def __len__(self):
        return self._size

    # ------------------------------------------------------------------
    def __repr__(self):
        parts = [f"{n}({w})" for n, w in self]
        return " -> ".join(parts) + " -> NULL"
