"""
vertex.py
---------
Represents a single vertex (building/location) of the campus graph.

Keeping Vertex as its own small class (rather than just a string key)
lets us cleanly attach algorithm-time metadata to it (distance, visited
flag, previous-node pointer for path reconstruction) without polluting
the Graph class itself.
"""


class Vertex:
    """A graph vertex representing one campus location."""

    def __init__(self, name, x=0, y=0):
        self.name = name
        self.x = x                 # pixel x-coordinate on the map (from config.py)
        self.y = y                 # pixel y-coordinate on the map
        self.adjacency = None      # LinkedList of AdjacencyNode, set by Graph

        # --- Algorithm bookkeeping fields (reset before every run) -----
        self.visited = False
        self.distance = float("inf")
        self.previous = None       # name of the previous vertex on shortest path

    def reset(self):
        """Reset algorithm bookkeeping fields before a fresh run."""
        self.visited = False
        self.distance = float("inf")
        self.previous = None

    def __repr__(self):
        return f"Vertex({self.name})"

    def __lt__(self, other):
        # Needed so Vertex objects can be compared inside the MinHeap
        # when distances are tied.
        return self.name < other.name
