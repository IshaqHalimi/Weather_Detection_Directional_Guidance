# ishaq halimi
# CMPSC 463 Project 2
# Keeping the entry file small makes it very clear where execution begins.
# December 5th, 2025

import tkinter as tk
from gui import WeatherGuidanceApp

"""
Create the Tkinter window, attach our WeatherGuidanceApp,
and start the GUI event loop.

This is the single function you call to run the whole project.
"""
def main() -> None:

    root = tk.Tk()
    app = WeatherGuidanceApp(root)
    root.mainloop()


if __name__ == "__main__":
    # When this file is ran directly (python main.py),
    # we call main() to start the program.
    main()