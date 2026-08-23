"""
algorithms.py
-------------
Core graph algorithms for the campus navigation educator app.
"""

import time
from queue_ds import Queue
from stack import Stack
from minheap import MinHeap


def _snapshot_heap(heap):
    return [(priority, item) for priority, item in heap._data]


def _snapshot_queue(queue):
    items = []
    node = queue._front
    while node is not None:
        items.append(node.data)
        node = node.next
    return items


def _snapshot_stack(stack):
    items = []
    node = stack._top
    while node is not None:
        items.append(node.data)
        node = node.next
    return items


def _meta(name, purpose, ds, time_complexity, space_complexity, use_case):
    return {
        "name": name,
        "purpose": purpose,
        "data_structure": ds,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "use_case": use_case,
    }


def dijkstra(graph, source, destination):
    graph.reset_all()
    start_time = time.perf_counter()

    steps = []
    visited_order = []

    graph.vertices[source].distance = 0
    heap = MinHeap()
    heap.push(0, source)

    while not heap.is_empty():
        dist_u, u = heap.pop_min()
        vertex_u = graph.vertices[u]

        if vertex_u.visited:
            continue

        vertex_u.visited = True
        visited_order.append(u)
        steps.append({
            "type": "visit",
            "node": u,
            "heap_state": _snapshot_heap(heap),
            "adjacency": list(graph.get_neighbours(u)),
        })

        if u == destination:
            break

        for neighbour, weight in graph.get_neighbours(u):
            v = graph.vertices[neighbour]
            steps.append({
                "type": "relax_attempt",
                "u": u,
                "v": neighbour,
                "heap_state": _snapshot_heap(heap),
                "adjacency": list(graph.get_neighbours(u)),
            })

            if v.visited:
                continue

            new_dist = vertex_u.distance + weight
            if new_dist < v.distance:
                v.distance = new_dist
                v.previous = u
                heap.push(new_dist, neighbour)
                steps.append({
                    "type": "relax_success",
                    "u": u,
                    "v": neighbour,
                    "new_dist": new_dist,
                    "heap_state": _snapshot_heap(heap),
                    "adjacency": list(graph.get_neighbours(u)),
                })

    exec_time = time.perf_counter() - start_time

    path = []
    dest_vertex = graph.vertices[destination]
    if dest_vertex.distance != float("inf"):
        cur = destination
        while cur is not None:
            path.append(cur)
            cur = graph.vertices[cur].previous
        path.reverse()

    return {
        "path": path,
        "distance": dest_vertex.distance,
        "visited_order": visited_order,
        "steps": steps,
        "exec_time": exec_time,
        "meta": _meta(
            "Dijkstra",
            "Shortest weighted path",
            "Priority Queue (Min Heap)",
            "O((V+E) log V)",
            "O(V)",
            "Weighted routing and shortest path problems",
        ),
    }


def bfs(graph, source, destination=None):
    graph.reset_all()
    start_time = time.perf_counter()

    steps = []
    visited_order = []

    q = Queue()
    graph.vertices[source].visited = True
    q.enqueue(source)
    visited_order.append(source)
    steps.append({
        "type": "visit",
        "node": source,
        "queue_state": _snapshot_queue(q),
        "adjacency": list(graph.get_neighbours(source)),
    })

    found = destination is None

    while not q.is_empty():
        u = q.dequeue()
        if u == destination:
            found = True
            break

        for neighbour, weight in graph.get_neighbours(u):
            steps.append({
                "type": "explore_edge",
                "u": u,
                "v": neighbour,
                "queue_state": _snapshot_queue(q),
                "adjacency": list(graph.get_neighbours(u)),
            })
            v = graph.vertices[neighbour]
            if not v.visited:
                v.visited = True
                v.previous = u
                visited_order.append(neighbour)
                q.enqueue(neighbour)
                steps.append({
                    "type": "visit",
                    "node": neighbour,
                    "queue_state": _snapshot_queue(q),
                    "adjacency": list(graph.get_neighbours(neighbour)),
                })

    exec_time = time.perf_counter() - start_time

    path = []
    if destination is not None and found:
        cur = destination
        while cur is not None:
            path.append(cur)
            cur = graph.vertices[cur].previous
        path.reverse()

    return {
        "path": path,
        "visited_order": visited_order,
        "steps": steps,
        "exec_time": exec_time,
        "found": found,
        "meta": _meta(
            "BFS",
            "Explores level by level",
            "Queue",
            "O(V+E)",
            "O(V)",
            "Shortest hop-count traversal",
        ),
    }


def dfs(graph, source, destination=None):
    graph.reset_all()
    start_time = time.perf_counter()

    steps = []
    visited_order = []

    st = Stack()
    st.push(source)

    found = destination is None

    while not st.is_empty():
        u = st.pop()
        vertex_u = graph.vertices[u]

        if vertex_u.visited:
            continue

        vertex_u.visited = True
        visited_order.append(u)
        steps.append({
            "type": "visit",
            "node": u,
            "stack_state": _snapshot_stack(st),
            "adjacency": list(graph.get_neighbours(u)),
        })

        if u == destination:
            found = True
            break

        neighbours = list(graph.get_neighbours(u))
        for neighbour, weight in reversed(neighbours):
            v = graph.vertices[neighbour]
            steps.append({
                "type": "explore_edge",
                "u": u,
                "v": neighbour,
                "stack_state": _snapshot_stack(st),
                "adjacency": list(graph.get_neighbours(u)),
            })
            if not v.visited:
                if v.previous is None:
                    v.previous = u
                st.push(neighbour)

    exec_time = time.perf_counter() - start_time

    path = []
    if destination is not None and found:
        cur = destination
        while cur is not None:
            path.append(cur)
            cur = graph.vertices[cur].previous
        path.reverse()

    return {
        "path": path,
        "visited_order": visited_order,
        "steps": steps,
        "exec_time": exec_time,
        "found": found,
        "meta": _meta(
            "DFS",
            "Explores as far as possible before backtracking",
            "Stack",
            "O(V+E)",
            "O(V)",
            "Backtracking and path exploration",
        ),
    }
