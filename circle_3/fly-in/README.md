*This project has been created as part of the 42 curriculum by mouaguil.*

# Fly-in

## Description

Fly-in is a Python simulation that routes a fleet of drones from one start
hub to one end hub through a network of connected zones. The objective is to
deliver every drone in as few simulation turns as possible while respecting
zone types, zone capacities, connection capacities, blocked areas, and
two-turn movement into restricted zones.

The project contains a strict map parser, an object-oriented graph model, a
custom pathfinder, a turn-by-turn scheduler, the required textual movement
output, and an optional colored terminal replay of the completed simulation.

## Features

- Parses the complete map format with line-specific error messages.
- Supports normal, priority, restricted, and blocked zones.
- Enforces zone and bidirectional connection capacities.
- Schedules simultaneous movements without collisions or deadlocks.
- Distributes drones over equal-cost paths when this improves throughput.
- Prioritizes priority zones when route costs are otherwise equal.
- Caches pathfinding results used repeatedly during scheduling.
- Produces the exact movement format required by the subject.
- Displays a dependency-free colored map directly in the terminal.

## Instructions

### Requirements

- Python 3.10 or later
- GNU Make
- Internet access during the first dependency installation, unless the
  packages are already cached

### Installation

From the project root, run:

```bash
make install
```

This installs the pinned development tools from `requirements.txt` for the
current user. No root access is needed. The simulator and terminal visualizer
themselves use only the Python standard library.

### Running the simulator

```bash
make run MAP=map.txt
```

Replace `map.txt` with any compatible map path. When `MAP` is omitted, the
Makefile uses the root `map.txt` file.

### Running the visualizer

```bash
make visual MAP=map.txt
```

The same terminal map updates once per simulation turn and waits one second
between turns. Each frame replaces the previous frame instead of adding a new
map to the terminal. Pressing `Ctrl+C` stops visual mode cleanly.

### Debugging and quality checks

```bash
make debug MAP=map.txt
make lint
make lint-strict
make clean
```

- `debug` starts the simulator with Python's built-in `pdb` debugger.
- `lint` runs the mandatory Flake8 and Mypy commands from the subject.
- `lint-strict` runs the optional strict Mypy check.
- `clean` removes project `__pycache__` directories and `.mypy_cache`.

## Map Format

A map begins with a positive drone count, followed by zones and then
connections:

```text
nb_drones: 3
start_hub: start 0 0 [color=green]
hub: middle 1 0 [zone=priority max_drones=2 color=purple]
end_hub: end 2 0 [color=yellow]
connection: start-middle [max_link_capacity=2]
connection: middle-end
```

Metadata is optional. Zone names cannot contain spaces or dashes, and
comments begin with `#`.

## Simulation Output

Each output line represents one turn. Only drones that move during that turn
are printed, and simultaneous movements are separated by spaces:

```text
D1-middle D2-middle
D1-end D2-end D3-middle
D3-end
```

A departure toward a restricted zone identifies the traversed connection.
The following turn records the mandatory arrival at that restricted zone.

## Algorithm and Implementation Strategy

The parser converts input text into `Graph`, `Zone`, and `Connection` objects.
The graph stores adjacency lists so the rest of the program never needs to
work with raw map lines.

`PathFinder` implements Dijkstra's algorithm without any external graph
library. Entering a normal or priority zone costs one turn, entering a
restricted zone costs two turns, and blocked zones are excluded. When two
routes have the same movement cost, the route containing more priority zones
is preferred.

`Simulator` processes each turn in two stages:

1. It plans a compatible collection of movements using projected zone and
   connection occupancy.
2. It commits every accepted movement simultaneously.

Projected occupancy allows one drone to enter a zone during the same turn
that another drone leaves it. Restricted departures reserve capacity at the
future destination, guaranteeing that the drone can arrive on the following
turn without waiting on the connection. If a preferred first step is full,
the simulator asks the pathfinder for a temporary alternative, which spreads
drones across useful parallel routes.

One new shortest-path computation uses `O(V^2 + E)` time and `O(V + E)`
working memory, where `V` is the number of zones and `E` the number of
connections. Results are cached by start zone and avoided-zone set, reducing
repeated calculations during later turns.

## Visual Representation

The terminal visualizer consumes the simulator's completed movement history;
it does not calculate separate routes. It applies all movements from one turn
together, updates one persistent terminal map, and waits one second before the
next turn. Restricted departures highlight their connection and the following
turn records the mandatory arrival.

The terminal map displays:

- Every zone and bidirectional connection using the map coordinates
- `S`, `E`, `o`, `P`, `R`, and `X` for unoccupied zone states
- A drone count in place of the zone symbol whenever a zone is occupied
- `*` when more than nine drones share the start or end zone
- Highlighted connections used during the current turn
- Current turn, total turns, delivery progress, and movement tokens

Map colors are mapped into a consistent seven-color visual palette. Unknown
single-word color names are assigned deterministically, so every valid color
metadata value still receives visible feedback.

Keeping the graph in the same screen position makes the replay easier to
follow because the user's eyes do not need to find the map again after every
turn. Replacing an occupied zone's type symbol with its drone count makes
congestion and simultaneous movement visible immediately. The progress bar,
highlighted active connections, and colored movement tokens connect the raw
simulator output to what is happening on the network, so routing decisions and
zone-state changes can be understood without reading every output line alone.

## Project Structure

```text
src/models/          Graph, zone, connection, drone, and enums
src/parsing/         Map parser and parsing exceptions
src/pathfinding/     Custom Dijkstra pathfinder
src/simulation/      Turn planning and movement scheduling
src/visualization/   ANSI terminal map and color theme
src/main.py          Command-line entry point
```

## Resources

- [Python documentation](https://docs.python.org/3/)
- [Python pdb documentation](https://docs.python.org/3/library/pdb.html)
- [Mypy documentation](https://mypy.readthedocs.io/en/stable/)
- [Flake8 documentation](https://flake8.pycqa.org/en/latest/)

### Use of AI

AI was used as a collaborative tool to review the subject, discuss the object
model and scheduling strategy, identify parser and simulator mistakes, explain
capacity reservations and path selection, design and test the terminal
visualizer, verify benchmark outputs, improve the Makefile, and prepare the
documentation. Every suggestion was reviewed and tested against the subject;
the project owner remains responsible for understanding the implementation.
