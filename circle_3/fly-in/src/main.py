"""Command-line entry point for the Fly-in drone simulation."""

from __future__ import annotations

import sys

from src.parsing.exceptions import MapParseError
from src.parsing.parser import MapParser
from src.simulation.simulator import SimulationError, Simulator
from src.visualization.visualizer import (
    TerminalVisualizer,
    VisualizationError,
)

SUCCESS = 0
RUNTIME_ERROR = 1
USAGE_ERROR = 2
USAGE = "Usage: python3 -m src.main <map_file> [--visual]"


def main(arguments: list[str] | None = None) -> int:
    """Parse one map, run its simulation, and print movement turns.

    Args:
        arguments: Command-line arguments without the program name. When
            omitted, arguments are read from ``sys.argv``.

    Returns:
        SUCCESS on completion, RUNTIME_ERROR for a map or simulation error,
        or USAGE_ERROR when exactly one map path was not provided.
    """
    if arguments is None:
        arguments = sys.argv[1:]

    if not (
        len(arguments) == 1
        or (len(arguments) == 2 and arguments[1] == "--visual")
    ):
        print(USAGE, file=sys.stderr)
        return USAGE_ERROR

    map_path = arguments[0]
    visual_mode = len(arguments) == 2
    try:
        graph, nb_drones = MapParser().parse(map_path)
        history = Simulator(graph, nb_drones).run()
    except (MapParseError, SimulationError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return RUNTIME_ERROR

    if visual_mode:
        try:
            TerminalVisualizer(graph, nb_drones).animate(history)
        except KeyboardInterrupt:
            return SUCCESS
        except VisualizationError as error:
            print(f"Error: {error}", file=sys.stderr)
            return RUNTIME_ERROR
    else:
        for turn_movements in history:
            print(" ".join(turn_movements))

    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
