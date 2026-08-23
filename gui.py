"""
gui.py
------
Tkinter front-end for the Pulchowk Smart Campus Navigation System.
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

import config
from graph import Graph
from algorithms import dijkstra, bfs, dfs


class CampusNavigatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PULCHOWK SMART CAMPUS NAVIGATION SYSTEM")
        self.root.geometry("1500x900")
        self.root.configure(bg="#F4F1EA")
        self.root.resizable(True, True)
        self.root.minsize(1300, 820)

        try:
            self.graph = Graph.from_config(config.NODES, config.EDGES)
        except ValueError as exc:
            messagebox.showerror("Configuration Error", str(exc))
            self.graph = Graph()
            for name, (x, y) in config.NODES.items():
                self.graph.add_vertex(name, x, y)
            for u, v, w in config.EDGES:
                self.graph.add_edge(u, v, w)

        self.scale_x = config.CANVAS_DISPLAY_SIZE[0] / config.MAP_IMAGE_SIZE[0]
        self.scale_y = config.CANVAS_DISPLAY_SIZE[1] / config.MAP_IMAGE_SIZE[1]

        self.click_mode = "source"
        self.node_canvas_ids = {}
        self.edge_canvas_ids = {}
        self.edge_weight_labels = {}
        self.exec_time_history = {"Dijkstra": None, "BFS": None, "DFS": None}
        self.animation_running = False
        self.current_result = None
        self.current_algorithm = "Dijkstra"
        self.result_vars = {
            "exec_time": tk.StringVar(value="Execution Time: --"),
            "traversal": tk.StringVar(value="Traversal: --"),
            "path": tk.StringVar(value="Shortest Path: --"),
            "distance": tk.StringVar(value="Distance: --"),
            "walk_time": tk.StringVar(value="Walking Time: --"),
        }

        self._build_layout()
        self._draw_map_and_graph()
        self._refresh_graph_information()

    def _build_layout(self):
        self.root.columnconfigure(0, weight=3)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=0)

        left_frame = tk.Frame(self.root, bg="#F4F1EA")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=12, pady=12)
        left_frame.columnconfigure(0, weight=1)
        left_frame.rowconfigure(1, weight=1)

        title = tk.Label(left_frame, text="ICTC Side Campus Map", font=("Segoe UI", 14, "bold"), bg="#F4F1EA")
        title.grid(row=0, column=0, sticky="w")

        self.canvas = tk.Canvas(left_frame, width=config.CANVAS_DISPLAY_SIZE[0], height=config.CANVAS_DISPLAY_SIZE[1], highlightthickness=1, highlightbackground="#999")
        self.canvas.grid(row=1, column=0, pady=(6, 6))
        self.canvas.bind("<Button-1>", self._on_canvas_click)

        legend = tk.Frame(left_frame, bg="#F4F1EA")
        legend.grid(row=2, column=0, sticky="w")
        self._build_legend(legend)

        right_frame = tk.Frame(self.root, bg="#FFFFFF", bd=1, relief="solid")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(0, 12), pady=12)

        self._build_controls(right_frame)
        self._build_information_panels(right_frame)

        status_frame = tk.Frame(self.root, bg="#F3F3F3", bd=1, relief="solid")
        status_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=12, pady=(0, 12))
        self.status_var = tk.StringVar(value="Ready")
        tk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 10), bg="#F3F3F3", anchor="w").pack(fill="x", padx=12, pady=8)

    def _build_legend(self, parent):
        for color, label in [(config.COLOR_NODE_NORMAL, "Normal"), (config.COLOR_NODE_VISITED, "Visited"), (config.COLOR_NODE_PROCESSING, "Processing"), (config.COLOR_NODE_DESTINATION, "Destination"), (config.COLOR_NODE_FINAL_PATH, "Final Path")]:
            swatch = tk.Label(parent, bg=color, width=2, height=1, bd=1, relief="solid")
            swatch.pack(side="left", padx=(0, 4))
            tk.Label(parent, text=label, bg="#F4F1EA", font=("Segoe UI", 9)).pack(side="left", padx=(0, 10))

    def _build_controls(self, parent):
        pad = {"padx": 12, "pady": 6}
        tk.Label(parent, text="Route Controls", font=("Segoe UI", 14, "bold"), bg="#FFFFFF").pack(anchor="w", **pad)

        names = self.graph.get_vertex_names()
        tk.Label(parent, text="Source", bg="#FFFFFF", font=("Segoe UI", 10)).pack(anchor="w", padx=12)
        self.source_var = tk.StringVar(value=names[0])
        ttk.Combobox(parent, textvariable=self.source_var, values=names, state="readonly").pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(parent, text="Destination", bg="#FFFFFF", font=("Segoe UI", 10)).pack(anchor="w", padx=12)
        self.dest_var = tk.StringVar(value=names[-1])
        ttk.Combobox(parent, textvariable=self.dest_var, values=names, state="readonly").pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(parent, text="Algorithm", bg="#FFFFFF", font=("Segoe UI", 10)).pack(anchor="w", padx=12)
        self.algo_var = tk.StringVar(value="Dijkstra")
        ttk.Combobox(parent, textvariable=self.algo_var, values=["Dijkstra", "BFS", "DFS"], state="readonly").pack(fill="x", padx=12, pady=(0, 8))

        tk.Label(parent, text="Animation Speed", bg="#FFFFFF", font=("Segoe UI", 10)).pack(anchor="w", padx=12)
        self.speed_var = tk.StringVar(value="Normal")
        ttk.Combobox(parent, textvariable=self.speed_var, values=["Slow", "Normal", "Fast"], state="readonly").pack(fill="x", padx=12, pady=(0, 8))

        btn_frame = tk.Frame(parent, bg="#FFFFFF")
        btn_frame.pack(fill="x", padx=12, pady=(4, 8))
        self.find_btn = tk.Button(btn_frame, text="Find Route", bg="#0B1F66", fg="white", font=("Segoe UI", 10, "bold"), command=self.on_find_route)
        self.find_btn.pack(side="left", fill="x", expand=True, padx=(0, 4))
        self.reset_btn = tk.Button(btn_frame, text="Reset", bg="#9A9A9A", fg="white", font=("Segoe UI", 10, "bold"), command=self.on_reset)
        self.reset_btn.pack(side="left", fill="x", expand=True, padx=(4, 0))
        self.skip_btn = tk.Button(parent, text="Skip Animation", bg="#E63946", fg="white", font=("Segoe UI", 9, "bold"), command=self.on_skip_animation)
        self.skip_btn.pack(fill="x", padx=12, pady=(0, 8))
        self.run_all_btn = tk.Button(parent, text="Run All & Compare", bg="#3EA644", fg="white", font=("Segoe UI", 9, "bold"), command=self.on_run_all)
        self.run_all_btn.pack(fill="x", padx=12, pady=(0, 8))
        self.chart_btn = tk.Button(parent, text="Show Performance Chart", bg="#2E6BE6", fg="white", font=("Segoe UI", 9, "bold"), command=self.on_show_chart)
        self.chart_btn.pack(fill="x", padx=12, pady=(0, 8))
        self.adj_btn = tk.Button(parent, text="Show Adjacency List", bg="#6C63FF", fg="white", font=("Segoe UI", 9, "bold"), command=self.on_show_adjacency_list)
        self.adj_btn.pack(fill="x", padx=12, pady=(0, 8))

    def _build_information_panels(self, parent):
        ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=12, pady=8)

        info_frame = tk.LabelFrame(parent, text="Algorithm Information", bg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=8, pady=8)
        info_frame.pack(fill="x", padx=12, pady=(0, 8))
        self.algorithm_info_var = tk.StringVar(value="Dijkstra\nUses Priority Queue (Min Heap)\nPurpose: Shortest weighted path\nTime Complexity: O((V+E) log V)\nSpace Complexity: O(V)")
        tk.Label(info_frame, textvariable=self.algorithm_info_var, justify="left", anchor="w", bg="#FFFFFF", font=("Segoe UI", 9), wraplength=320).pack(anchor="w")

        results_frame = tk.LabelFrame(parent, text="Live Results", bg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=8, pady=8)
        results_frame.pack(fill="x", padx=12, pady=(0, 8))
        self.live_results_text = tk.Text(results_frame, height=10, width=42, font=("Segoe UI", 9), wrap="word")
        self.live_results_text.pack(fill="both")
        self.live_results_text.configure(state="disabled")

        inspector_frame = tk.LabelFrame(parent, text="Data Structure Inspector", bg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=8, pady=8)
        inspector_frame.pack(fill="x", padx=12, pady=(0, 8))
        self.inspector_text = tk.Text(inspector_frame, height=10, width=42, font=("Segoe UI", 9), wrap="word")
        self.inspector_text.pack(fill="both")
        self.inspector_text.configure(state="disabled")

        building_frame = tk.LabelFrame(parent, text="Building Information", bg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=8, pady=8)
        building_frame.pack(fill="x", padx=12, pady=(0, 8))
        self.building_info_text = tk.Text(building_frame, height=8, width=42, font=("Segoe UI", 9), wrap="word")
        self.building_info_text.pack(fill="both")
        self.building_info_text.configure(state="disabled")

        results_frame = tk.LabelFrame(parent, text="Results", bg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=8, pady=8)
        results_frame.pack(fill="x", padx=12, pady=(0, 8))
        for key in ["exec_time", "traversal", "path", "distance", "walk_time"]:
            tk.Label(results_frame, textvariable=self.result_vars[key], justify="left", anchor="w", bg="#FFFFFF", font=("Segoe UI", 9), wraplength=320).pack(anchor="w", pady=2)

        graph_frame = tk.LabelFrame(parent, text="Graph Information", bg="#FFFFFF", font=("Segoe UI", 11, "bold"), padx=8, pady=8)
        graph_frame.pack(fill="x", padx=12, pady=(0, 8))
        self.graph_info_var = tk.StringVar(value="")
        tk.Label(graph_frame, textvariable=self.graph_info_var, justify="left", anchor="w", bg="#FFFFFF", font=("Segoe UI", 9), wraplength=320).pack(anchor="w")

    def _draw_map_and_graph(self):
        pil_img = Image.open(config.MAP_IMAGE_PATH).convert("RGB")
        pil_img = pil_img.resize(config.CANVAS_DISPLAY_SIZE, Image.LANCZOS)
        self.map_photo = ImageTk.PhotoImage(pil_img)
        self.canvas.create_image(0, 0, anchor="nw", image=self.map_photo)

        for edge in self.graph.edges:
            x1, y1 = self._to_canvas_coords(edge.u)
            x2, y2 = self._to_canvas_coords(edge.v)
            line_id = self.canvas.create_line(x1, y1, x2, y2, fill=config.COLOR_EDGE_NORMAL, width=3)
            self.edge_canvas_ids[frozenset((edge.u, edge.v))] = line_id
            edge.canvas_id = line_id
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            text_id = self.canvas.create_text(mx, my, text=str(edge.weight), font=("Segoe UI", 7, "bold"), fill="#333")
            self.edge_weight_labels[line_id] = text_id
            self.canvas.itemconfigure(text_id, state="hidden")
            self.canvas.tag_bind(line_id, "<Enter>", lambda e, line_id=line_id, text_id=text_id: self._show_edge_weight(line_id, text_id))
            self.canvas.tag_bind(line_id, "<Leave>", lambda e, text_id=text_id: self._hide_edge_weight(text_id))

        r = config.NODE_RADIUS
        for name in self.graph.get_vertex_names():
            x, y = self._to_canvas_coords(name)
            oval_id = self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=config.COLOR_NODE_NORMAL, outline="#333333", width=1.5)
            self.node_canvas_ids[name] = oval_id
            self.canvas.tag_bind(oval_id, "<Enter>", lambda e, name=name: self._show_hover(name, e))
            self.canvas.tag_bind(oval_id, "<Leave>", lambda e: self._hide_hover())

        self._refresh_source_destination_highlights()

    def _to_canvas_coords(self, name):
        vx, vy = config.NODES[name]
        return vx * self.scale_x, vy * self.scale_y

    def _show_edge_weight(self, line_id, text_id):
        self.canvas.itemconfigure(text_id, state="normal")

    def _hide_edge_weight(self, text_id):
        self.canvas.itemconfigure(text_id, state="hidden")

    def _show_hover(self, name, event):
        x, y = config.NODES[name]
        neighbours = list(self.graph.get_neighbours(name))
        connected = ", ".join([n for n, _ in neighbours]) if neighbours else "None"
        detail = f"{name}\nCoordinates: ({x}, {y})\nConnected buildings: {connected}\nDegree: {len(neighbours)}"
        self.tooltip_label = tk.Label(self.root, text=detail, bg="#FFF8C2", relief="solid", bd=1, font=("Segoe UI", 9), justify="left")
        self.tooltip_label.place(x=event.x_root + 12, y=event.y_root + 8)

    def _hide_hover(self):
        if hasattr(self, "tooltip_label"):
            self.tooltip_label.place_forget()

    def _on_canvas_click(self, event):
        clicked = self._find_clicked_node(event.x, event.y)
        if clicked is None:
            return
        self._show_building_details(clicked)
        if self.click_mode == "source":
            self.source_var.set(clicked)
            self.click_mode = "destination"
            self.status_var.set(f"Source set to '{clicked}'. Click again for destination.")
        else:
            self.dest_var.set(clicked)
            self.click_mode = "source"
            self.status_var.set(f"Destination set to '{clicked}'. Ready to find route.")
        self._refresh_source_destination_highlights()

    def _find_clicked_node(self, cx, cy):
        r = config.NODE_RADIUS
        for name in self.graph.get_vertex_names():
            x, y = self._to_canvas_coords(name)
            if (cx - x) ** 2 + (cy - y) ** 2 <= r ** 2:
                return name
        return None

    def _show_building_details(self, name):
        vertex = self.graph.vertices[name]
        neighbours = list(vertex.adjacency)
        connected = ", ".join([n for n, _ in neighbours]) if neighbours else "None"
        adjacency_lines = [f"{name}", "↓"]
        for neighbour, weight in neighbours:
            adjacency_lines.append(f"{neighbour} ({weight})")
            adjacency_lines.append("↓")
        adjacency_lines.append("NULL")
        self.building_info_text.configure(state="normal")
        self.building_info_text.delete("1.0", "end")
        self.building_info_text.insert("end", f"Building: {name}\nCoordinates: ({vertex.x}, {vertex.y})\nConnected buildings: {connected}\nDegree: {len(neighbours)}\n\nAdjacency list:\n" + "\n".join(adjacency_lines))
        self.building_info_text.configure(state="disabled")

    def _refresh_source_destination_highlights(self):
        source = self.source_var.get()
        destination = self.dest_var.get()
        for name, oval_id in self.node_canvas_ids.items():
            outline = "#333333"
            width = 1.5
            if name == source:
                outline = "#111111"
                width = 3.0
            elif name == destination:
                outline = "#E63946"
                width = 2.2
            self.canvas.itemconfig(oval_id, outline=outline, width=width)

    def _repaint_static(self):
        for name, oval_id in self.node_canvas_ids.items():
            self.canvas.itemconfig(oval_id, fill=config.COLOR_NODE_NORMAL)
        self._refresh_source_destination_highlights()
        for line_id, text_id in self.edge_weight_labels.items():
            self.canvas.itemconfigure(text_id, state="hidden")

    def _set_node_state(self, name, state):
        oval_id = self.node_canvas_ids[name]
        if state == "visited":
            fill = config.COLOR_NODE_VISITED
        elif state == "processing":
            fill = config.COLOR_NODE_PROCESSING
        elif state == "final":
            fill = config.COLOR_NODE_FINAL_PATH
        elif state == "destination":
            fill = config.COLOR_NODE_DESTINATION
        else:
            fill = config.COLOR_NODE_NORMAL
        self.canvas.itemconfig(oval_id, fill=fill)

    def _refresh_graph_information(self):
        components = self.graph.connected_components()
        density = len(self.graph.edges) / (len(self.graph.vertices) * (len(self.graph.vertices) - 1) / 2) if len(self.graph.vertices) > 1 else 0
        self.graph_info_var.set(f"Vertices: {len(self.graph.vertices)}\nEdges: {len(self.graph.edges)}\nDensity: {density:.2f}\nConnected components: {len(components)}")

    def on_reset(self):
        if self.animation_running:
            return
        self._repaint_static()
        self.result_vars["exec_time"].set("Execution Time: --")
        self.result_vars["traversal"].set("Traversal: --")
        self.result_vars["path"].set("Shortest Path: --")
        self.result_vars["distance"].set("Distance: --")
        self.result_vars["walk_time"].set("Walking Time: --")
        self._update_live_results({"type": "visit", "node": "--", "u": "--", "v": "--"}, self.current_algorithm)
        self.status_var.set("Ready")
        self.click_mode = "source"

    def on_find_route(self):
        if self.animation_running:
            return
        source = self.source_var.get()
        dest = self.dest_var.get()
        algo = self.algo_var.get()
        if source == dest:
            messagebox.showwarning("Invalid selection", "Source and Destination must be different.")
            return
        self._repaint_static()
        self._set_node_state(dest, "destination")
        self._refresh_source_destination_highlights()
        self.current_algorithm = algo
        if algo == "Dijkstra":
            result = dijkstra(self.graph, source, dest)
        elif algo == "BFS":
            result = bfs(self.graph, source, dest)
        else:
            result = dfs(self.graph, source, dest)
        self.current_result = result
        self.exec_time_history[algo] = result["exec_time"]
        self._update_algorithm_info(algo, result)
        self._update_results(result, algo)
        self._animate_steps(result["steps"], result.get("path", []), result, algo)

    def on_skip_animation(self):
        if self.current_result is None:
            return
        self._highlight_final_path(self.current_result.get("path", []))
        self._update_results(self.current_result, self.current_algorithm)
        self.status_var.set("Animation skipped")
        self.animation_running = False

    def on_run_all(self):
        self._repaint_static()
        results = {}
        for algo in ["Dijkstra", "BFS", "DFS"]:
            source = self.source_var.get()
            dest = self.dest_var.get()
            if algo == "Dijkstra":
                result = dijkstra(self.graph, source, dest)
            elif algo == "BFS":
                result = bfs(self.graph, source, dest)
            else:
                result = dfs(self.graph, source, dest)
            results[algo] = result
            self.exec_time_history[algo] = result["exec_time"]
        self.on_show_chart(results=results)

    def on_show_adjacency_list(self):
        win = tk.Toplevel(self.root)
        win.title("Adjacency List")
        text = tk.Text(win, width=60, height=24, font=("Segoe UI", 10))
        text.pack(fill="both", expand=True, padx=8, pady=8)
        text.insert("end", self.graph.print_adjacency_list())
        text.configure(state="disabled")

    def _update_algorithm_info(self, algo, result):
        if algo == "Dijkstra":
            info = "Dijkstra\nUses Priority Queue (Min Heap)\nPurpose: Shortest weighted path\nTime Complexity: O((V+E) log V)\nSpace Complexity: O(V)\nTypical use: Weighted routing"
        elif algo == "BFS":
            info = "BFS\nUses Queue\nPurpose: Level-by-level search\nTime Complexity: O(V+E)\nSpace Complexity: O(V)\nTypical use: Shortest hop-count traversal"
        else:
            info = "DFS\nUses Stack\nPurpose: Deep exploration before backtracking\nTime Complexity: O(V+E)\nSpace Complexity: O(V)\nTypical use: Path exploration and backtracking"
        self.algorithm_info_var.set(info)

    def _update_results(self, result, algo):
        path = result.get("path", [])
        if algo == "Dijkstra":
            distance = result.get("distance", float("inf"))
            if not path or distance == float("inf"):
                self.result_vars["path"].set("Shortest Path: No path found")
                self.result_vars["distance"].set("Distance: --")
                self.result_vars["walk_time"].set("Walking Time: --")
            else:
                self.result_vars["path"].set("Shortest Path:\n" + "\n↓\n".join(path))
                self.result_vars["distance"].set(f"Distance: {distance} m")
                minutes = distance / config.WALKING_SPEED_M_PER_MIN
                self.result_vars["walk_time"].set(f"Walking Time: {minutes:.1f} min")
        else:
            found = result.get("found", bool(path))
            if not found or not path:
                self.result_vars["path"].set("Shortest Path: No path found")
                self.result_vars["distance"].set("Distance: --")
                self.result_vars["walk_time"].set("Walking Time: --")
            else:
                total_dist = self._path_distance(path)
                self.result_vars["path"].set("Shortest Path:\n" + "\n↓\n".join(path))
                self.result_vars["distance"].set(f"Distance: {total_dist} m (not distance-optimal)")
                minutes = total_dist / config.WALKING_SPEED_M_PER_MIN
                self.result_vars["walk_time"].set(f"Walking Time: {minutes:.1f} min")
        self.result_vars["exec_time"].set(f"Execution Time: {result['exec_time'] * 1000:.4f} ms")
        self.result_vars["traversal"].set("Traversal: " + " -> ".join(result.get("visited_order", [])))

    def _path_distance(self, path):
        total = 0
        for i in range(len(path) - 1):
            total += self.graph.vertices[path[i]].adjacency.get_weight(path[i + 1])
        return total

    def _animate_steps(self, steps, final_path, result, algo):
        self.animation_running = True
        self.find_btn.config(state="disabled")
        self.skip_btn.config(state="normal")
        self._animate_index(steps, 0, final_path, result, algo)

    def _animate_index(self, steps, i, final_path, result, algo):
        if i >= len(steps):
            self._highlight_final_path(final_path)
            self.animation_running = False
            self.find_btn.config(state="normal")
            self.skip_btn.config(state="disabled")
            self.status_var.set("Animation complete")
            return

        step = steps[i]
        self._apply_step(step, algo)
        delay = {"Slow": 800, "Normal": 450, "Fast": 120}[self.speed_var.get()]
        self.canvas.after(delay, lambda: self._animate_index(steps, i + 1, final_path, result, algo))

    def _apply_step(self, step, algo):
        t = step["type"]
        if t == "visit":
            node = step["node"]
            self._set_node_state(node, "processing")
            self._update_live_results(step, algo)
            self.status_var.set(f"Visiting {node}")
            self.canvas.after(120, lambda: self._settle_visited(node))
        elif t in ("relax_attempt", "explore_edge"):
            u, v = step["u"], step["v"]
            self._update_live_results(step, algo)
            self.status_var.set(f"Checking edge {u} → {v}")
            key = frozenset((u, v))
            if key in self.edge_canvas_ids:
                self.canvas.itemconfig(self.edge_canvas_ids[key], fill=config.COLOR_EDGE_RELAXING, width=4)
        elif t == "relax_success":
            u, v, nd = step["u"], step["v"], step["new_dist"]
            self._update_live_results(step, algo)
            self.status_var.set(f"Relaxing {u} → {v} with distance {nd}")

    def _settle_visited(self, node):
        if node == self.dest_var.get():
            self._set_node_state(node, "destination")
        else:
            self._set_node_state(node, "visited")
        self._refresh_source_destination_highlights()

    def _highlight_final_path(self, path):
        if not path:
            return
        for name in path:
            self._set_node_state(name, "final")
        for i in range(len(path) - 1):
            key = frozenset((path[i], path[i + 1]))
            if key in self.edge_canvas_ids:
                self.canvas.itemconfig(self.edge_canvas_ids[key], fill=config.COLOR_EDGE_FINAL_PATH, width=5)
        self._refresh_source_destination_highlights()

    def _update_live_results(self, step, algo):
        if algo == "Dijkstra":
            state = step.get("heap_state", [])
            ds_repr = "Priority Queue\n" + "\n".join([f"{priority} {node}" for priority, node in state]) if state else "Priority Queue\n(empty)"
            current_node = step.get("node") or step.get("u") or "--"
            current_edge = f"{step.get('u')} → {step.get('v')}" if step.get('u') else "--"
            current_distance = step.get("new_dist") if step.get("new_dist") is not None else "--"
        elif algo == "BFS":
            state = step.get("queue_state", [])
            ds_repr = "Queue\nFRONT\n" + "\n".join(state) + "\nREAR" if state else "Queue\n(empty)"
            current_node = step.get("node") or step.get("u") or "--"
            current_edge = f"{step.get('u')} → {step.get('v')}" if step.get('u') else "--"
            current_distance = "--"
        else:
            state = step.get("stack_state", [])
            ds_repr = "Stack\nTOP\n" + "\n".join(state) + "\nBOTTOM" if state else "Stack\n(empty)"
            current_node = step.get("node") or step.get("u") or "--"
            current_edge = f"{step.get('u')} → {step.get('v')}" if step.get('u') else "--"
            current_distance = "--"
        adjacency = list(self.graph.get_neighbours(current_node)) if current_node != "--" else []
        adjacency_text = "Adjacency list\n" + "\n".join([f"{n} ({w})" for n, w in adjacency]) if adjacency else "Adjacency list\n(empty)"
        text = (
            f"Current Node: {current_node}\n"
            f"Visited Count: {len(self.graph.vertices)}\n"
            f"Current Distance: {current_distance}\n"
            f"Current Edge: {current_edge}\n"
            f"Data Structure Size: {len(state) if 'state' in locals() else 0}\n\n"
            f"{ds_repr}\n\n"
            f"{adjacency_text}"
        )
        self.live_results_text.configure(state="normal")
        self.live_results_text.delete("1.0", "end")
        self.live_results_text.insert("end", text)
        self.live_results_text.configure(state="disabled")
        self.inspector_text.configure(state="normal")
        self.inspector_text.delete("1.0", "end")
        self.inspector_text.insert("end", ds_repr + "\n\n" + adjacency_text)
        self.inspector_text.configure(state="disabled")

    def on_show_chart(self, results=None):
        import matplotlib
        matplotlib.use("TkAgg")
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        if results is None:
            labels, values = [], []
            for algo, t in self.exec_time_history.items():
                if t is not None:
                    labels.append(algo)
                    values.append(t * 1000)
            if not labels:
                messagebox.showinfo("No data", "Run at least one algorithm first to compare execution times.")
                return
        else:
            labels = ["Dijkstra", "BFS", "DFS"]
            values = [results[algo]["exec_time"] * 1000 for algo in labels]

        chart_win = tk.Toplevel(self.root)
        chart_win.title("Performance Comparison")
        fig, ax = plt.subplots(figsize=(6, 4))
        colors = {"Dijkstra": "#0B1F66", "BFS": "#3EA644", "DFS": "#F4C430"}
        ax.bar(labels, values, color=[colors.get(l, "#2E6BE6") for l in labels])
        ax.set_ylabel("Execution Time (ms)")
        ax.set_title("Algorithm Performance Comparison")
        for i, v in enumerate(values):
            ax.text(i, v, f"{v:.4f}", ha="center", va="bottom", fontsize=9)
        fig.tight_layout()
        note = tk.Label(chart_win, text="Execution times are illustrative. The theoretical complexity differences become more significant on larger graphs.", wraplength=500, justify="center", font=("Segoe UI", 9), fg="#555")
        note.pack(fill="x", padx=10, pady=(6, 0))
        canvas = FigureCanvasTkAgg(fig, master=chart_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        plt.close(fig)
