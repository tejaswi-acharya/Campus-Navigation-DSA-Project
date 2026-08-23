"""
config.py
---------
Central configuration file for the Pulchowk Smart Campus Navigation System.
This keeps the graph data separate from the algorithm logic and GUI code.
"""

MAP_IMAGE_PATH = "assets/campus_map.png"
MAP_IMAGE_SIZE = (1254, 1254)
CANVAS_DISPLAY_SIZE = (700, 700)

NODES = {
    "Main Entry": (930, 785),
    "Dean Office": (220, 295),
    "Robotics Club": (490, 245),
    "DoEC": (880, 250),
    "ICTC Building": (1070, 650),
    "Library": (760, 800),
    "Canteen": (270, 875),
}

EDGES = [
    ("Main Entry", "Library", 17),
    ("Main Entry", "ICTC Building", 19),
    ("Main Entry", "Dean Office", 28),
    ("Main Entry", "DoEC", 35),
    ("Library", "DoEC", 56),
    ("Library", "Canteen", 50),
    ("DoEC", "Robotics Club", 39),
    ("Robotics Club", "Dean Office", 27),
    ("Dean Office", "Canteen", 58),
    ("DoEC", "ICTC Building", 44),
    ("Library", "ICTC Building", 32),
    ("Robotics Club", "ICTC Building", 42),
    ("Dean Office", "Library", 44),
    ("DoEC", "Canteen", 51),
]

WALKING_SPEED_M_PER_MIN = 80

COLOR_NODE_NORMAL = "#2E6BE6"
COLOR_NODE_VISITED = "#3EA644"
COLOR_NODE_PROCESSING = "#F4C430"
COLOR_NODE_DESTINATION = "#E63946"
COLOR_NODE_SOURCE = "#111111"
COLOR_NODE_FINAL_PATH = "#0B1F66"

COLOR_EDGE_NORMAL = "#9A9A9A"
COLOR_EDGE_RELAXING = "#F4C430"
COLOR_EDGE_FINAL_PATH = "#0B1F66"

NODE_RADIUS = 12
FONT_LABEL = ("Segoe UI", 9, "bold")
ANIMATION_DELAY_MS = 550
