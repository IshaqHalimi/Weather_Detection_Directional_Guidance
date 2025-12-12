# Weather Detection & Directional Guidance
## Project Overview

Weather Detection & Directional Guidance is an interactive system that models the Penn State Abington campus as a weighted graph.
The system simulates random weather events such as tornado warnings, flooding, and fallen debris, which temporarily block certain paths.
By selecting a starting point and a destination, users can compute the shortest safe route, even when the usual paths are blocked due to weather conditions.
The project combines algorithmic rigor with user-friendly visualization to create a tool that is both educational and practical.

## Key Features
- Graph-based campus model: Nodes represent locations and edges represent walkable paths with associated travel times.
- Dynamic weather simulation: Random weather events block certain paths in real-time.
- Shortest-path computation: Uses Dijkstra’s algorithm to find the fastest available route.
- Interactive GUI: Tkinter interface allows users to select start/destination nodes, simulate weather, and visualize routes.
- Real-time feedback: Blocked paths are shown in red, calculated routes in cyan, and start/end nodes are highlighted for clarity.

## Code Structure
The project is organized into three modular Python files:
- logic.py:	Defines the campus graph, weather-event randomizer, and implements Dijkstra’s algorithm.
- gui.py:	Implements the Tkinter interface, including map visualization, clickable nodes, edge weight labels, and route highlighting.
- main.py:	Launches the GUI and initializes the application.

## Installation & Execution

Follow these steps to run the Weather Detection & Directional Guidance project:

### Clone the repository
Open your terminal or command prompt and run:
git clone https://github.com/IshaqHalimi/Weather_Detection_Directional_Guidance



### avigate to the project directory
cd weather-detection-guidance


### Ensure Python is installed
Make sure you have Python 3.x installed. You can check by running:

python --version

or

python3 --version


### Install required packages
This project uses Tkinter, which is usually included with Python. If Tkinter is not installed, you can install it via your system’s package manager. For example:

- Windows: Tkinter comes pre-installed.
- macOS: Tkinter comes with Python 3.x.
- Linux (Ubuntu/Debian): sudo apt-get install python3-tk


### Run the program
Execute the main script to launch the GUI:

python main.py

or

python3 main.py


### Interact with the GUI
- Click on the campus map to select your start and destination nodes.
- Press “Randomizer” to simulate weather events.
- Press “Find Route” to compute the safest path.
- Use Reset to clear the map and start again.