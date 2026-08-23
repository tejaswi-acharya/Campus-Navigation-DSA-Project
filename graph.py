"""
graph.py
--------
The Graph class and configuration validation for the educational campus app.
"""

from linkedlist import LinkedList
from vertex import Vertex
from edge import Edge


def validate_configuration(nodes, edges):
    """Validate the graph configuration and return a list of user-facing errors."""
    errors = []
    if not nodes:
        return ["Configuration Error: No vertices were defined."]

    valid_vertices = set(nodes.keys())
    seen_edges = set()

    for name, coords in nodes.items():
        if not isinstance(coords, tuple) or len(coords) != 2:
            errors.append(f"Configuration Error: Vertex '{name}' must have (x, y) coordinates.")
            continue
        x, y = coords
        if not isinstance(x, (int, float)) or not isinstance(y, (int, float)):
            errors.append(f"Configuration Error: Vertex '{name}' coordinates must be numeric.")

    for idx, edge in enumerate(edges, start=1):
        if len(edge) != 3:
            errors.append(f"Configuration Error: Edge #{idx} must be a (u, v, weight) tuple.")
            continue
        u, v, weight = edge
        if u == v:
            errors.append(f"Configuration Error: Self-loop detected at edge #{idx}: '{u}'.")
        if u not in valid_vertices:
            errors.append(f"Configuration Error: Vertex '{u}' referenced in edge #{idx} was not found in NODES.")
        if v not in valid_vertices:
            errors.append(f"Configuration Error: Vertex '{v}' referenced in edge #{idx} was not found in NODES.")
        if not isinstance(weight, (int, float)) or weight <= 0:
            errors.append(f"Configuration Error: Edge '{u}' - '{v}' must have a positive numeric weight.")

        pair = frozenset((u, v))
        if pair in seen_edges:
            errors.append(f"Configuration Error: Duplicate edge detected: '{u}' - '{v}'.")
        else:
            seen_edges.add(pair)

    return errors


class Graph:
    """An undirected, weighted graph built from Vertex + LinkedList."""

    def __init__(self):
        self.vertices = {}
        self.edges = []

    @classmethod
    def from_config(cls, nodes, edges):
        errors = validate_configuration(nodes, edges)
        if errors:
            raise ValueError("\n".join(errors))

        graph = cls()
        for name, (x, y) in nodes.items():
            graph.add_vertex(name, x, y)
        for u_name, v_name, weight in edges:
            graph.add_edge(u_name, v_name, weight)
        return graph

    def add_vertex(self, name, x=0, y=0):
        if name not in self.vertices:
            v = Vertex(name, x, y)
            v.adjacency = LinkedList()
            self.vertices[name] = v
        return self.vertices[name]

    def add_edge(self, u_name, v_name, weight):
        if u_name not in self.vertices or v_name not in self.vertices:
            raise ValueError(f"Both vertices must exist before adding edge ({u_name} - {v_name})")
        if u_name == v_name:
            raise ValueError("Self-loops are not allowed")
        if self._has_edge(u_name, v_name):
            raise ValueError(f"Duplicate edge detected: {u_name} - {v_name}")

        self.vertices[u_name].adjacency.append(v_name, weight)
        self.vertices[v_name].adjacency.append(u_name, weight)
        self.edges.append(Edge(u_name, v_name, weight))

    def _has_edge(self, u_name, v_name):
        for edge in self.edges:
            if edge.connects(u_name, v_name):
                return True
        return False

    def get_neighbours(self, name):
        return self.vertices[name].adjacency

    def get_vertex_names(self):
        return list(self.vertices.keys())

    def reset_all(self):
        for v in self.vertices.values():
            v.reset()

    def connected_components(self):
        visited = set()
        components = []
        for name in self.vertices:
            if name in visited:
                continue
            stack = [name]
            visited.add(name)
            component = []
            while stack:
                current = stack.pop()
                component.append(current)
                for neighbour, _ in self.get_neighbours(current):
                    if neighbour not in visited:
                        visited.add(neighbour)
                        stack.append(neighbour)
            components.append(component)
        return components

    def print_adjacency_list(self):
        lines = []
        for name, vertex in self.vertices.items():
            lines.append(f"{name}\n  -> {vertex.adjacency}")
        return "\n".join(lines)

    def __repr__(self):
        return f"Graph(vertices={len(self.vertices)}, edges={len(self.edges)})"
