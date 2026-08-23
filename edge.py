"""
edge.py
-------
A tiny value object representing one edge (road/path) between two
campus buildings. Mostly used by the GUI layer to keep track of which
canvas line-id corresponds to which (u, v) pair, so it can be recoloured
during animation (gray -> yellow -> dark blue).
"""


class Edge:
    """Represents an undirected weighted edge between two vertices."""

    __slots__ = ("u", "v", "weight", "canvas_id")

    def __init__(self, u, v, weight):
        self.u = u
        self.v = v
        self.weight = weight
        self.canvas_id = None      # Tkinter canvas item id, set by the GUI

    def connects(self, a, b):
        """True if this edge connects vertices `a` and `b` (either order)."""
        return (self.u == a and self.v == b) or (self.u == b and self.v == a)

    def __repr__(self):
        return f"Edge({self.u} <-> {self.v}, w={self.weight})"
