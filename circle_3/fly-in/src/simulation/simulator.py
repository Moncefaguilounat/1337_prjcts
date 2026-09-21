"""Turn-by-turn movement scheduling for the Fly-in drone network."""

from __future__ import annotations

from dataclasses import dataclass

from src.models.connection import Connection
from src.models.drone import Drone
from src.models.enums import ZoneType
from src.models.graph import Graph
from src.pathfinding.pathfinder import PathFinder


class SimulationError(RuntimeError):
    """Raised when a valid simulation cannot continue or be initialized."""


@dataclass(frozen=True)
class MoveIntent:
    """A validated movement that will be committed during the current turn.

    The simulator plans movements before changing the real graph state. This
    small record keeps the information needed to apply one accepted movement.
    """

    drone: Drone
    source_name: str
    destination_name: str
    connection: Connection
    starts_transit: bool


class Simulator:
    """Move every drone from the start zone to the end zone safely.

    A turn has two stages: first the simulator plans legal movements using
    projected capacities, then it commits every accepted movement. Planning
    before mutation allows a drone to enter a zone that another accepted
    drone leaves during the same turn.
    """

    def __init__(self, graph: Graph, nb_drones: int) -> None:
        """Prepare a fresh simulation for a parsed graph.

        Args:
            graph: Parsed network containing one start and one end zone.
            nb_drones: Positive number of drones that begin at the start.

        Raises:
            SimulationError: If the graph is incomplete, already occupied,
                or has no route from start to end.
        """
        self.graph = graph
        self.pathfinder = PathFinder(graph)
        self.turn_number = 0
        self.history: list[list[str]] = []
        self._reserved_arrivals: dict[str, int] = {}
        self._path_cache: dict[
            tuple[str, frozenset[str]], list[str] | None
        ] = {}

        self._validate_initial_state(nb_drones)
        self.drones = self._create_drones(nb_drones)

    def run(self) -> list[list[str]]:
        """Run turns until every drone reaches the end zone.

        Returns:
            A copy of the complete movement history, grouped by turn.

        Raises:
            SimulationError: If the simulation becomes deadlocked.
        """
        while not self.is_complete():
            self.step()

        return [list(turn) for turn in self.history]

    def step(self) -> list[str]:
        """Execute one complete simulation turn.

        Returns:
            Movement tokens for this turn, ordered by drone number. Waiting
            drones are omitted. Calling step after completion returns [].

        Raises:
            SimulationError: If unfinished drones cannot make progress.
        """
        if self.is_complete():
            return []

        self.turn_number += 1
        movements: dict[str, str] = {}

        arrived_this_turn = self._advance_in_transit_drones(movements)
        intents = self._plan_waiting_drones(arrived_this_turn)
        self._commit_intents(intents, movements)

        ordered_movements = [
            movements[drone.drone_id]
            for drone in self.drones
            if drone.drone_id in movements
        ]
        self._raise_if_stalled(ordered_movements)
        self.history.append(ordered_movements)
        return list(ordered_movements)

    def is_complete(self) -> bool:
        """Return True when every drone has been delivered."""
        return all(drone.is_delivered() for drone in self.drones)

    def _validate_initial_state(self, nb_drones: int) -> None:
        """Validate the graph and drone count before creating runtime state."""
        if nb_drones <= 0:
            raise SimulationError("nb_drones must be a positive integer.")
        if self.graph.start_zone_name is None:
            raise SimulationError("The graph has no start zone.")
        if self.graph.end_zone_name is None:
            raise SimulationError("The graph has no end zone.")

        if any(zone.occupants for zone in self.graph.zones.values()):
            raise SimulationError("The graph already contains drones.")
        if any(
            connection.occupants
            for connection in self.graph.connections.values()
        ):
            raise SimulationError(
                "The graph already has occupied connections."
            )

        route = self.pathfinder.shortest_path(
            self.graph.start_zone_name,
            self.graph.end_zone_name,
        )
        if route is None:
            raise SimulationError("No route exists from start to end.")

    def _create_drones(self, nb_drones: int) -> list[Drone]:
        """Create all drones and register them inside the start zone."""
        start_name = self._start_name()
        start_zone = self.graph.get_zone(start_name)
        drones: list[Drone] = []

        for number in range(1, nb_drones + 1):
            drone = Drone(f"D{number}", start_name)
            start_zone.add_drone(drone.drone_id)
            drones.append(drone)

        return drones

    def _advance_in_transit_drones(
        self, movements: dict[str, str]
    ) -> set[str]:
        """Advance flying drones and complete arrivals that are due now.

        Returns:
            IDs of drones that arrived this turn. They are excluded from
            ordinary planning because one drone may act only once per turn.
        """
        arrived: set[str] = set()

        for drone in self.drones:
            if not drone.is_in_transit():
                continue
            if drone.connection_key is None or drone.target_zone is None:
                raise SimulationError(
                    f"{drone.drone_id} has incomplete transit information."
                )

            connection = self.graph.connections.get(drone.connection_key)
            if connection is None:
                raise SimulationError(
                    f"{drone.drone_id} references an unknown connection."
                )
            target_name = drone.target_zone

            if not drone.advance_transit():
                source_name = connection.other_end(target_name)
                movements[drone.drone_id] = self._connection_token(
                    drone, source_name, target_name
                )
                continue

            target_zone = self.graph.get_zone(target_name)
            if not target_zone.is_end and not target_zone.has_capacity():
                raise SimulationError(
                    f"Reserved arrival for {drone.drone_id} cannot enter "
                    f"zone '{target_name}'."
                )

            connection.leave(drone.drone_id)
            self._release_arrival_reservation(target_name)
            drone.arrive(target_name, target_zone.is_end)
            if not target_zone.is_end:
                target_zone.add_drone(drone.drone_id)

            movements[drone.drone_id] = (
                f"{drone.drone_id}-{target_name}"
            )
            arrived.add(drone.drone_id)

        return arrived

    def _plan_waiting_drones(
        self, excluded_drone_ids: set[str]
    ) -> list[MoveIntent]:
        """Plan a compatible set of moves without mutating real occupancy."""
        zone_counts = {
            name: len(zone.occupants)
            for name, zone in self.graph.zones.items()
        }
        connection_usage = {
            key: len(connection.occupants)
            for key, connection in self.graph.connections.items()
        }
        reservations = dict(self._reserved_arrivals)
        intents: list[MoveIntent] = []

        waiting_drones = [
            drone
            for drone in self.drones
            if not drone.is_delivered()
            and not drone.is_in_transit()
            and drone.drone_id not in excluded_drone_ids
        ]
        waiting_drones.sort(key=self._planning_priority)

        for drone in waiting_drones:
            path = self._find_immediately_available_path(
                drone, zone_counts, connection_usage, reservations
            )
            if path is None:
                continue

            source_name = path[0]
            destination_name = path[1]
            connection = self.graph.get_connection(
                source_name, destination_name
            )
            destination = self.graph.get_zone(destination_name)
            intent = MoveIntent(
                drone=drone,
                source_name=source_name,
                destination_name=destination_name,
                connection=connection,
                starts_transit=(
                    destination.zone_type is ZoneType.RESTRICTED
                ),
            )
            self._reserve_projected_capacity(
                intent, zone_counts, connection_usage, reservations
            )
            intents.append(intent)

        return intents

    def _find_immediately_available_path(
        self,
        drone: Drone,
        zone_counts: dict[str, int],
        connection_usage: dict[frozenset[str], int],
        reservations: dict[str, int],
    ) -> list[str] | None:
        """Find a path whose first movement is legal during this turn.

        When the preferred first zone is unavailable, it is temporarily
        avoided and the pathfinder is asked for an alternative. This simple
        retry is what allows drones to spread across parallel routes.
        """
        if drone.current_zone is None:
            raise SimulationError(
                f"Waiting drone {drone.drone_id} has no current zone."
            )

        avoided_zones: set[str] = set()
        end_name = self._end_name()

        while True:
            path = self._shortest_path(drone.current_zone, avoided_zones)
            if path is None or len(path) < 2:
                return None

            destination_name = path[1]
            connection = self.graph.get_connection(
                drone.current_zone, destination_name
            )
            if self._has_projected_capacity(
                destination_name,
                connection,
                zone_counts,
                connection_usage,
                reservations,
            ):
                alternative = self._less_loaded_equal_cost_path(
                    drone.current_zone,
                    path,
                    avoided_zones,
                    zone_counts,
                    connection_usage,
                    reservations,
                )
                if alternative is not None:
                    return alternative
                return path

            if destination_name == end_name:
                return None
            avoided_zones.add(destination_name)

    def _less_loaded_equal_cost_path(
        self,
        source_name: str,
        preferred_path: list[str],
        avoided_zones: set[str],
        zone_counts: dict[str, int],
        connection_usage: dict[frozenset[str], int],
        reservations: dict[str, int],
    ) -> list[str] | None:
        """Return an equal-cost route when its first zone is less loaded."""
        preferred_destination = preferred_path[1]
        alternative = self._shortest_path(
            source_name, avoided_zones | {preferred_destination}
        )
        if alternative is None or len(alternative) < 2:
            return None
        if self._path_cost(alternative) != self._path_cost(preferred_path):
            return None

        alternative_destination = alternative[1]
        alternative_connection = self.graph.get_connection(
            source_name, alternative_destination
        )
        if not self._has_projected_capacity(
            alternative_destination,
            alternative_connection,
            zone_counts,
            connection_usage,
            reservations,
        ):
            return None

        preferred = self.graph.get_zone(preferred_destination)
        alternative_zone = self.graph.get_zone(alternative_destination)
        preferred_load = (
            zone_counts[preferred_destination]
            + reservations.get(preferred_destination, 0)
        )
        alternative_load = (
            zone_counts[alternative_destination]
            + reservations.get(alternative_destination, 0)
        )
        if (
            alternative_load * preferred.max_drones
            < preferred_load * alternative_zone.max_drones
        ):
            return alternative
        return None

    def _has_projected_capacity(
        self,
        destination_name: str,
        connection: Connection,
        zone_counts: dict[str, int],
        connection_usage: dict[frozenset[str], int],
        reservations: dict[str, int],
    ) -> bool:
        """Check destination and connection capacity in the planned turn."""
        connection_count = connection_usage[connection.key()]
        if connection_count >= connection.max_link_capacity:
            return False

        destination = self.graph.get_zone(destination_name)
        if destination.is_start or destination.is_end:
            return True

        occupied = zone_counts[destination_name]
        reserved = reservations.get(destination_name, 0)
        return occupied + reserved < destination.max_drones

    def _reserve_projected_capacity(
        self,
        intent: MoveIntent,
        zone_counts: dict[str, int],
        connection_usage: dict[frozenset[str], int],
        reservations: dict[str, int],
    ) -> None:
        """Update temporary counts after accepting a movement intent."""
        zone_counts[intent.source_name] -= 1
        connection_key = intent.connection.key()
        connection_usage[connection_key] += 1

        destination = self.graph.get_zone(intent.destination_name)
        if intent.starts_transit and not destination.is_end:
            reservations[intent.destination_name] = (
                reservations.get(intent.destination_name, 0) + 1
            )
        elif not destination.is_end:
            zone_counts[intent.destination_name] += 1

    def _commit_intents(
        self,
        intents: list[MoveIntent],
        movements: dict[str, str],
    ) -> None:
        """Apply accepted movements after all capacity planning is complete."""
        for intent in intents:
            source = self.graph.get_zone(intent.source_name)
            source.remove_drone(intent.drone.drone_id)

        for intent in intents:
            destination = self.graph.get_zone(intent.destination_name)
            if intent.starts_transit:
                intent.connection.enter(intent.drone.drone_id)
                future_turns = destination.move_cost() - 1
                intent.drone.start_transit(
                    intent.connection.key(),
                    intent.destination_name,
                    future_turns,
                )
                if not destination.is_end:
                    self._reserved_arrivals[intent.destination_name] = (
                        self._reserved_arrivals.get(
                            intent.destination_name, 0
                        )
                        + 1
                    )
                movements[intent.drone.drone_id] = self._connection_token(
                    intent.drone,
                    intent.source_name,
                    intent.destination_name,
                )
                continue

            intent.drone.arrive(
                intent.destination_name, destination.is_end
            )
            if not destination.is_end:
                destination.add_drone(intent.drone.drone_id)
            movements[intent.drone.drone_id] = (
                f"{intent.drone.drone_id}-{intent.destination_name}"
            )

    def _planning_priority(self, drone: Drone) -> tuple[int, int]:
        """Prioritize drones nearest to the end, then lower drone numbers."""
        if drone.current_zone is None:
            raise SimulationError(
                f"Waiting drone {drone.drone_id} has no current zone."
            )
        path = self._shortest_path(drone.current_zone, set())
        if path is None:
            raise SimulationError(
                f"No route from '{drone.current_zone}' to the end for "
                f"{drone.drone_id}."
            )
        return self._path_cost(path), self._drone_number(drone)

    def _shortest_path(
        self, start_name: str, avoided_zones: set[str]
    ) -> list[str] | None:
        """Return a cached shortest path for a start and avoidance set."""
        cache_key = (start_name, frozenset(avoided_zones))
        if cache_key not in self._path_cache:
            self._path_cache[cache_key] = self.pathfinder.shortest_path(
                start_name,
                self._end_name(),
                avoided_zones,
            )
        cached_path = self._path_cache[cache_key]
        return list(cached_path) if cached_path is not None else None

    def _path_cost(self, path: list[str]) -> int:
        """Return the total destination-zone movement cost of a path."""
        return sum(
            self.graph.get_zone(zone_name).move_cost()
            for zone_name in path[1:]
        )

    def _release_arrival_reservation(self, zone_name: str) -> None:
        """removes reservation when an in-transit drone arrives."""
        zone = self.graph.get_zone(zone_name)
        if zone.is_end:
            return

        reservation_count = self._reserved_arrivals.get(zone_name, 0)
        if reservation_count <= 0:
            raise SimulationError(
                f"Zone '{zone_name}' has no reservation for an arrival."
            )
        if reservation_count == 1:
            del self._reserved_arrivals[zone_name]
        else:
            self._reserved_arrivals[zone_name] = reservation_count - 1

    def _raise_if_stalled(self, movements: list[str]) -> None:
        """Raise a clear error if unfinished drones made no progress."""
        if movements or self.is_complete():
            return
        raise SimulationError(
            f"Simulation is deadlocked at turn {self.turn_number}."
        )

    def _start_name(self) -> str:
        """Return the validated start-zone name."""
        if self.graph.start_zone_name is None:
            raise SimulationError("The graph has no start zone.")
        return self.graph.start_zone_name

    def _end_name(self) -> str:
        """Return the validated end-zone name."""
        if self.graph.end_zone_name is None:
            raise SimulationError("The graph has no end zone.")
        return self.graph.end_zone_name

    @staticmethod
    def _drone_number(drone: Drone) -> int:
        """Return the numeric part of a generated ID such as D12."""
        return int(drone.drone_id[1:])

    @staticmethod
    def _connection_token(
        drone: Drone, source_name: str, destination_name: str
    ) -> str:
        """Format movement onto a connection toward a restricted zone."""
        return (
            f"{drone.drone_id}-{source_name}-{destination_name}"
        )
