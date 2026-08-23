"""
main.py
-------
Entry point for the Pulchowk Smart Campus Navigation System.

Run with:
    python3 main.py

Make sure you run this from inside the `project/` directory (or that the
`assets/campus_map.png` path in config.py is adjusted accordingly).
"""

import tkinter as tk
from gui import CampusNavigatorApp


def main():
    root = tk.Tk()
    app = CampusNavigatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
