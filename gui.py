# ishaq halimi
# CMPSC 463 Project 2
# Tkinter GUI for the 9-node PSU Abington campus graph.
# December 4th, 2025

import tkinter as tk

from logic import (
    NODE_LABELS,
    EDGES,
    edge_key,
    run_randomizer,
    dijkstra,
)

CANVAS_WIDTH = 1100
CANVAS_HEIGHT = 650
NODE_RADIUS = 20

# Spread-out layout, only for clarity
# PennState Abington campus reference
NODE_POS = {
    3: (120, 520),   # Lot J/H
    2: (320, 470),   # Lot G/F
    1: (540, 520),   # Sutherland
    6: (760, 470),   # Lares
    8: (980, 380),   # Spring House
    7: (980, 220),   # Woodland
    9: (760, 90),    # Rydal
    4: (320, 260),   # Athletic Building
    5: (540, 260),   # Tennis Field
}


class WeatherGuidanceApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Weather Detection & Directional Guidance")

        self.start = None
        self.end = None
        self.blocked_edges = set()
        self.current_path_edges = set()
        self.mode = "start"

        self._build_widgets()
        self._draw_graph()

    # UI layout

    def _build_widgets(self):
        top_frame = tk.Frame(self.root, bg="#111827")
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        tk.Button(
            top_frame, text="Select Start",
            command=self.set_mode_start, width=14
        ).grid(row=0, column=0, padx=3)

        tk.Button(
            top_frame, text="Select Destination",
            command=self.set_mode_end, width=18
        ).grid(row=0, column=1, padx=3)

        tk.Button(
            top_frame, text="Randomizer (Weather Event)",
            command=self.handle_randomizer, width=24
        ).grid(row=0, column=2, padx=3)

        tk.Button(
            top_frame, text="Reset Map",
            command=self.reset_map, width=12
        ).grid(row=0, column=3, padx=3)

        tk.Button(
            top_frame, text="Find Safest Route",
            command=self.find_route, width=18
        ).grid(row=0, column=4, padx=3)

        main_frame = tk.Frame(self.root, bg="#111827")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            main_frame,
            width=CANVAS_WIDTH,
            height=CANVAS_HEIGHT,
            bg="#020617",
            highlightthickness=0,
        )
        self.canvas.pack(side=tk.LEFT, padx=8, pady=8)

        legend = tk.Frame(main_frame, bg="#111827")
        legend.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.Y)

        tk.Label(
            legend, text="Campus Destinations",
            fg="white", bg="#111827",
            font=("TkDefaultFont", 10, "bold")
        ).pack(anchor="w")

        for nid in sorted(NODE_LABELS):
            tk.Label(
                legend,
                text=f"{nid}: {NODE_LABELS[nid]}",
                fg="white", bg="#111827"
            ).pack(anchor="w")

        self.status_label = tk.Label(
            self.root,
            text="Click a node (1–9) to set your current location (Start).",
            fg="white", bg="#111827"
        )
        self.status_label.pack(fill=tk.X)

        self.event_label = tk.Label(
            self.root,
            text="Event: none yet – press Randomizer to simulate weather.",
            fg="white", bg="#111827"
        )
        self.event_label.pack(fill=tk.X)

        self.route_label = tk.Label(
            self.root,
            text="Route: no route calculated yet.",
            fg="white", bg="#111827"
        )
        self.route_label.pack(fill=tk.X)

        self.root.configure(bg="#111827")
        self.canvas.bind("<Button-1>", self.on_canvas_click)

    # drawing

    def _draw_graph(self):
        self.canvas.delete("all")
        self.edge_items = {}
        self.node_items = {}

        # edges with weight labels
        for u, v, w in EDGES:
            x1, y1 = NODE_POS[u]
            x2, y2 = NODE_POS[v]
            ek = edge_key(u, v)

            color = self._edge_color(ek)
            width = 3 if ek in self.current_path_edges else 2

            line = self.canvas.create_line(
                x1, y1, x2, y2,
                fill=color,
                width=width
            )
            self.edge_items[ek] = line

            mx = (x1 + x2) / 2
            my = (y1 + y2) / 2
            self.canvas.create_text(
                mx, my,
                text=str(w),
                fill="white",
                font=("TkDefaultFont", 9),
            )

        # nodes
        for nid, (x, y) in NODE_POS.items():
            fill = self._node_color(nid)
            circle = self.canvas.create_oval(
                x - NODE_RADIUS, y - NODE_RADIUS,
                x + NODE_RADIUS, y + NODE_RADIUS,
                fill=fill, outline="#0f172a", width=2
            )
            text = self.canvas.create_text(
                x, y,
                text=str(nid),
                fill="white",
                font=("TkDefaultFont", 11, "bold")
            )
            self.node_items[nid] = (circle, text)

    def _edge_color(self, ek):
        if ek in self.blocked_edges:
            return "#b91c1c"  # red = closed
        if ek in self.current_path_edges:
            return "#38bdf8"  # cyan = chosen route
        return "#64748b"      # normal road

    def _node_color(self, nid):
        if self.start == nid:
            return "#22c55e"  # green
        if self.end == nid:
            return "#f97316"  # orange
        return "#1e293b"

    # mode switching

    def set_mode_start(self):
        self.mode = "start"
        self.status_label.config(
            text="Mode: Select Start – click a node (1–9) on the map."
        )

    def set_mode_end(self):
        self.mode = "end"
        self.status_label.config(
            text="Mode: Select Destination – click a node (1–9) on the map."
        )

    # interaction

    def on_canvas_click(self, event):
        clicked = None
        for nid, (x, y) in NODE_POS.items():
            dx = event.x - x
            dy = event.y - y
            if dx * dx + dy * dy <= NODE_RADIUS * NODE_RADIUS:
                clicked = nid
                break

        if clicked is None:
            self.status_label.config(
                text="Click directly on a node circle (1–9)."
            )
            return

        name = NODE_LABELS[clicked]
        if self.mode == "start":
            self.start = clicked
            self.status_label.config(
                text=f"Start set to: {clicked} – {name}. Now randomize weather or select destination."
            )
        else:
            self.end = clicked
            self.status_label.config(
                text=f"Destination set to: {clicked} – {name}. Click 'Find Safest Route'."
            )

        self.current_path_edges.clear()
        self._draw_graph()

    def handle_randomizer(self):
        event, blocked = run_randomizer(self.start, self.end)
        self.blocked_edges = blocked
        self.current_path_edges.clear()

        if event == "TORNADO":
            msg = f"Event: TORNADO WARNING – {len(blocked)} roads closed."
        elif event == "FLOODING":
            msg = f"Event: FLOODING – {len(blocked)} roads underwater."
        else:
            msg = f"Event: STORM DEBRIS – {len(blocked)} roads blocked."

        self.event_label.config(text=msg)
        self.route_label.config(text="Route: waiting for start + destination.")
        self._draw_graph()

    def find_route(self):
        if self.start is None:
            self.status_label.config(
                text="Select a start node first."
            )
            return
        if self.end is None:
            self.status_label.config(
                text="Select a destination node."
            )
            return

        path, total = dijkstra(self.start, self.end, self.blocked_edges)

        if not path:
            self.current_path_edges.clear()
            self.route_label.config(
                text="Route: No safe path exists – all routes are blocked."
            )
            self.status_label.config(
                text="Try another destination or reset the map."
            )
            self._draw_graph()
            return

        self.current_path_edges.clear()
        for i in range(len(path) - 1):
            self.current_path_edges.add(edge_key(path[i], path[i + 1]))

        path_str = " → ".join(str(n) for n in path)
        self.route_label.config(
            text=f"Route: {path_str}  |  Total time = {total} min"
        )
        self.status_label.config(
            text="Safest route highlighted in cyan; blocked roads are red."
        )
        self._draw_graph()

    def reset_map(self):
        self.start = None
        self.end = None
        self.blocked_edges.clear()
        self.current_path_edges.clear()

        self.event_label.config(
            text="Event: none yet – press Randomizer to simulate weather."
        )
        self.route_label.config(text="Route: no route calculated yet.")
        self.status_label.config(
            text="Map reset. Click a node (1–9) to set your current location (Start)."
        )
        self._draw_graph()