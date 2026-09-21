"""Shortest-path computation over the drone network (our own Dijkstra)."""

from __future__ import annotations

from src.models.enums import ZoneType
from src.models.graph import Graph


class PathFinder:
    """Finds the cheapest route between two zones in a Graph.

    This implements Dijkstra's algorithm by hand (no external graph
    library, as required by the subject). "Cheapest" means the lowest
    total turn cost, where entering a normal/priority zone costs 1
    turn and entering a restricted zone costs 2 turns; blocked zones
    are never considered.

    Among paths that cost the same number of turns, this PathFinder
    prefers the one that passes through more `priority` zones, since
    the subject says priority zones "should be prioritized in
    pathfinding" even though they don't cost less.
    """

    def __init__(self, graph: Graph) -> None:
        """Initialize a PathFinder bound to a specific Graph.

        Args:
            graph: The graph to search over.
        """

        self.graph = graph

    def shortest_path(
        self, start: str, end: str, avoid_zones: set[str] | None = None
    ) -> list[str] | None:
        """Compute the cheapest path from start to end.

        Args:
            start: Name of the starting zone.
            end: Name of the destination zone.
            avoid_zones: Optional set of zone names to route around
                (the end zone is never avoided, even if listed). This
                lets the simulator ask for an alternate route around
                a congested zone without duplicating this algorithm.

        Returns:
            A list of zone names from start to end (inclusive), or
            None if no valid path exists.

        Raises:
            ValueError: If start or end isn't a known zone name.
        """

        if start not in self.graph.zones:
            raise ValueError(f"Unknown zone: {start}")
        if end not in self.graph.zones:
            raise ValueError(f"Unknown zone: {end}")

        avoid = avoid_zones or set()

        distances: dict[str, int] = {start: 0}
        priority_pen: dict[str, int] = {start: 0}
        previous: dict[str, str | None] = {start: None}
        visited: set[str] = set()

        while True:
            current = self._pick_closest_unvisited(
                distances, priority_pen, visited
            )

            if current is None or current == end:
                break
            visited.add(current)
            self._relax_neighbors(current, avoid, end, distances,
                                  priority_pen, previous
                                  )

        if end not in distances:
            return None
        return self._reconstruct_path(previous, end)

    def _path_cost(self, path: list[str]) -> int:
        """Return the total turn cost of a previously computed path.

        Args:
            path: A list of zone names, e.g. the output of shortest_path().

        Returns:
            The sum of move costs for every zone after the first one
            (the drone is already standing in the first zone, so
            entering it is free).
        """

        total = 0
        for zone_name in path[1:]:
            total += self.graph.get_zone(zone_name).move_cost()
        return total

    def _relax_neighbors(
            self,
            current: str,
            avoid: set[str],
            end: str,
            distances: dict[str, int],
            priority_pen: dict[str, int],
            previous: dict[str, str | None],
    ) -> None:
        """Update distances/previous for every usable neighbor of `current`."""

        for neighbor_name in self.graph.neighbors(current):
            if neighbor_name in avoid and neighbor_name != end:
                continue

            neighbor = self.graph.get_zone(neighbor_name)

            if neighbor.is_blocked():
                continue

            c_distance = distances[current] + neighbor.move_cost()
            c_penalty = priority_pen[current]
            c_penalty += self._penalty_of(neighbor.zone_type)

            c_key = (c_distance, c_penalty)
            existing_distance = distances.get(neighbor_name)
            existing_penalty = priority_pen.get(neighbor_name)

            if (
                existing_distance is None
                or existing_penalty is None
                or c_key < (existing_distance, existing_penalty)
            ):
                distances[neighbor_name] = c_distance
                priority_pen[neighbor_name] = c_penalty
                previous[neighbor_name] = current

    @staticmethod
    def _penalty_of(zone_type: ZoneType) -> int:
        """Return the tie-break penalty for entering a zone of this type.

        Priority zones score 0 (no penalty); everything else scores 1.
        Lower total penalty wins ties on equal turn cost.
        """
        return 0 if zone_type is ZoneType.PRIORITY else 1

    @staticmethod
    def _pick_closest_unvisited(
        distances: dict[str, int],
        priority_pen: dict[str, int],
        visited: set[str],
    ) -> str | None:
        """Return the unvisited zone with the smallest (distance, penalty).

        Returns:
            The zone name to visit next, or None if every reachable
            zone has already been visited (the search is finished).
        """

        best_zone_name: str | None = None
        best_zone: tuple[int, int] | None = None

        for zone_name, distance in distances.items():
            if zone_name in visited:
                continue

            new_zone = (distance, priority_pen[zone_name])
            if best_zone is None or new_zone < best_zone:
                best_zone = new_zone
                best_zone_name = zone_name

        return best_zone_name

    @staticmethod
    def _reconstruct_path(previous: dict[str, str | None], end: str
                          ) -> list[str]:
        """Walk the `previous` chain backward from end to start."""

        path: list[str] = []
        current: str | None = end

        while current is not None:
            path.append(current)
            current = previous[current]
        path.reverse()
        return path
