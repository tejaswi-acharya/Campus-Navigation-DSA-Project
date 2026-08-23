# Pulchowk Smart Campus Navigation System

A Data Structures & Algorithms semester project that visualises graph
traversal and shortest-path algorithms over a real (static) map of the
ICTC side of Pulchowk Campus.

> **Scope note:** This is *not* meant to be a Google-Maps-style routing
> app. Its purpose is to make the mechanics of **Graphs, Linked Lists,
> Queues, Stacks, and a Priority Queue (Min-Heap)** visible and
> understandable, using BFS, DFS, and Dijkstra's algorithm as the
> demonstration vehicles.

---

## 1. Project Structure

```
project/
├── main.py            Entry point - launches the Tkinter app
├── graph.py            Graph class (adjacency list built from LinkedList)
├── linkedlist.py       Custom singly linked list (adjacency storage)
├── vertex.py            Vertex class (a campus building/location)
├── edge.py               Edge value object (used by the GUI for drawing)
├── queue_ds.py         Custom FIFO Queue (used by BFS)
├── stack.py               Custom LIFO Stack (used by DFS)
├── minheap.py           Custom binary Min-Heap (priority queue for Dijkstra)
├── algorithms.py     Dijkstra / BFS / DFS implementations
├── gui.py                   Tkinter GUI: map canvas, controls, animation
├── config.py             Node coordinates, edge list, colours, constants
├── assets/
│   └── campus_map.png   The provided static campus map (background layer)
└── README.md
```

Run it with:

```bash
cd project
python3 main.py
```

On Windows Command Prompt, activate the included virtual environment first:

```cmd
cd path\to\copy_project_dsa
.venv\Scripts\activate.bat
python main.py
```

On Windows PowerShell, use:

```powershell
cd path\to\copy_project_dsa
.\.venv\Scripts\Activate.ps1
python .\main.py
```

After activation, the terminal prompt starts with `(.venv)`. The application
opens as a Tkinter window, so the terminal may show no additional output.
Close the application window to stop it. (Requires Python 3, Tkinter, Pillow,
and Matplotlib.)

---

## 2. The Campus Graph

The campus is modelled as an **undirected, weighted graph**. Each vertex
is one of the seven ICTC-side buildings; each edge is a walkable path
between two buildings, weighted by its approximate distance in meters.

| Vertices (7)                              |
|--------------------------------------------|
| Main Entry, Dean Office, Robotics Club, DoEC, ICTC Building, Library, Canteen |

All coordinates and edge weights live in `config.py` — **never** hard-coded
inside `graph.py` or `algorithms.py`. This keeps the data cleanly separated
from the logic, so the same algorithms would work unmodified on a
completely different campus layout.

---

## 3. Data Structures — What's Implemented Manually, and Why

### 3.1 Linked List (`linkedlist.py`)

Each vertex's adjacency list is a genuine **singly linked list** of
`AdjacencyNode` objects (`neighbour`, `weight`, `next`), not a Python
list or dict. This mirrors the classic textbook adjacency-list diagram:

```
Library -> DoEC(56) -> Canteen(50) -> NULL
```

Supported operations: `append` (add edge), `remove` (delete edge),
`get_weight` (lookup), and iteration (`for neighbour, weight in list`).

- **Time complexity:** append O(n) (walks to the tail — could be O(1)
  with a tail pointer, but O(n) is fine given each vertex only has a
  handful of neighbours), search/remove O(n).
- **Space complexity:** O(E) total across all vertices, where E is the
  number of edges (each undirected edge contributes 2 adjacency nodes).

### 3.2 Graph (`graph.py`)

Wraps a dictionary of `Vertex` objects, each holding its own adjacency
`LinkedList`. `add_edge(u, v, w)` inserts into **both** u's and v's
linked lists, which is what makes the graph undirected.

- **Space complexity:** O(V + E)

### 3.3 Queue (`queue_ds.py`) — used by BFS

A linked-list-based FIFO queue with `head`/`tail` pointers, giving O(1)
`enqueue` and `dequeue`. (Named `queue_ds.py`, not `queue.py`, to avoid
clashing with Python's built-in `queue` module.)

### 3.4 Stack (`stack.py`) — used by DFS

A linked-list-based LIFO stack, O(1) `push`/`pop`. DFS is implemented
**iteratively** using this stack (rather than recursively), which is
both a clearer demonstration of the Stack data structure and avoids
Python's recursion depth limit.

### 3.5 Binary Min-Heap (`minheap.py`) — the Priority Queue for Dijkstra

An array-backed binary min-heap implemented from scratch: `push`
(insert + sift-up) and `pop_min` (remove root + sift-down), both
O(log n). Dijkstra uses **lazy deletion**: rather than implementing an
expensive decrease-key operation, a vertex may be pushed onto the heap
multiple times with different tentative distances; when popped, stale
entries (for already-finalised vertices) are simply skipped. This is a
standard, well-accepted simplification of the classic algorithm.

---

## 4. Algorithms (`algorithms.py`)

### 4.1 Breadth First Search (BFS)

Explores the graph level-by-level using the custom `Queue`. Finds the
path with the **fewest number of hops** between source and destination
(not necessarily the shortest by distance).

- **Time complexity:** O(V + E)
- **Space complexity:** O(V) for the visited flags + queue

### 4.2 Depth First Search (DFS)

Explores as far as possible along each branch before backtracking,
using the custom `Stack` (iterative, not recursive).

- **Time complexity:** O(V + E)
- **Space complexity:** O(V)

### 4.3 Dijkstra's Algorithm

Finds the **shortest-distance** path from source to destination using
the custom binary Min-Heap as its priority queue. At each step, the
vertex with the smallest tentative distance is popped and "relaxed"
against its neighbours; if a shorter path to a neighbour is found, its
distance is updated and it is pushed back onto the heap.

- **Time complexity:** O((V + E) log V) with a binary heap
- **Space complexity:** O(V)

Every algorithm records a list of **animation steps** (node visited,
edge relaxed/explored, etc.) which the GUI replays via
`canvas.after()`, and every algorithm is timed with
`time.perf_counter()` so its performance can be compared in the bar
chart (Matplotlib).

---

## 5. GUI (`gui.py`)

- **Left panel:** the supplied campus map image as the canvas
  background, with graph vertices drawn as clickable circles and edges
  drawn as lines, all positioned using the coordinates in `config.py`.
- **Right panel:** Source / Destination / Algorithm dropdowns, "Find
  Route" and "Reset" buttons, and a results area showing traversal
  order, shortest path, total distance, estimated walking time, and
  algorithm execution time.
- **Node colours:** Blue = normal, Yellow = currently processing,
  Green = visited, Red = destination, Dark Blue = final path.
- **Edge colours:** Gray = normal, Yellow = being relaxed/explored,
  Dark Blue = part of the final path.
- A **"Show Performance Comparison Chart"** button opens a Matplotlib
  bar chart comparing the execution times of whichever algorithms have
  been run so far in the session.

---

## 6. Summary Complexity Table

| Structure / Algorithm | Time Complexity      | Space Complexity |
|------------------------|-----------------------|-------------------|
| Linked List (append)   | O(n)                   | O(n)              |
| Queue (enqueue/dequeue)| O(1)                   | O(n)              |
| Stack (push/pop)       | O(1)                   | O(n)              |
| Binary Min-Heap        | O(log n) push/pop      | O(n)              |
| BFS                    | O(V + E)               | O(V)              |
| DFS                    | O(V + E)               | O(V)              |
| Dijkstra (binary heap) | O((V + E) log V)       | O(V)              |
