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

def _print_capacity_info(simulator) -> None:
    zone_usage = {
            zone_name: 0
            for zone_name in simulator.graph.zones
            }
    for drone in simulator.drones:
        if drone.current_zone is not None:
            zone_usage[drone.current_zone] += 1

    for zone_name, zone in simulator.graph.zones.items():
        capacity = (
                "unlimited"
                if zone.is_start or zone.is_end
                else str(zone.max_drones)
                )
        print(
                f"{zone_name}: "
                f"{zone_usage[zone_name]}/{capacity} drones"
                )
    for connection in simulator.graph.connections.values():
        print(
                f"{connection.zone_a}-{connection.zone_b}: "
                f"{len(connection.occupants)}/{connection.max_link_capacity} capacity used"
                )

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
        or (len(arguments) == 2 and arguments[1] == "--capacity-info")
    ):
        print(USAGE, file=sys.stderr)
        return USAGE_ERROR

    map_path = arguments[0]
    capacity_info_mode = len(arguments) == 2

    try:
        graph, nb_drones = MapParser().parse(map_path)
        simulator = Simulator(graph, nb_drones)
        if capacity_info_mode:
            while not simulator.is_complete():
                movements = simulator.step()
                print("______________________________")
                print(" ".join(movements))
                print("______________________________")
                _print_capacity_info(simulator)
        else:
            history = simulator.run()
    except (MapParseError, SimulationError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return RUNTIME_ERROR

    if capacity_info_mode:
        return SUCCESS

#    if visual_mode:
 #       try:
  #          TerminalVisualizer(graph, nb_drones).animate(history)
   #     except KeyboardInterrupt:
    #        return SUCCESS
     #   except VisualizationError as error:
      #      print(f"Error: {error}", file=sys.stderr)
       #     return RUNTIME_ERROR
   # else:
    #    for turn_movements in history:
     #       print(" ".join(turn_movements))

    return SUCCESS


if __name__ == "__main__":
    raise SystemExit(main())
