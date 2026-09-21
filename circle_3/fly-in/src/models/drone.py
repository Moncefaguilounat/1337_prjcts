"""The dorne model: a single agent moving through the graph"""

from src.models.enums import DroneState


class Drone:
    """A single drone traveling from the start zone to the end zone.

    A Drone tracks its own position and state, but does not decide
    where to go — that decision is made by the pathfinder/simulator
    and simply applied to the drone via these methods.

    Attributes:
        drone_id: Unique identifier, e.g. "D1".
        current_zone: Name of the zone the drone currently occupies,
            or None while it is mid-flight on a connection.
        state: The drone's current DroneState.
        transit_connection_key: Identifier of the connection being
            traversed, if any (used to release capacity on arrival).
        transit_target: Name of the zone the drone is flying toward,
            if currently in transit.
        transit_turns_remaining: Turns left before arrival, if in transit.
    """

    def __init__(self, drone_id: str, start_zone: str) -> None:
        """Initialize a Drone at the start zone.

        Args:
            drone_id: Unique identifier for this drone.
            start_zone: Name of the zone the drone begins in.
        """
        self.drone_id = drone_id
        self.current_zone: str | None = start_zone
        self.state: DroneState = DroneState.WAITING
        self.connection_key: frozenset[str] | None = None
        self.target_zone: str | None = None
        self.turns_remaining: int = 0

    def is_delivered(self) -> bool:
        """Return True if this drone has reached the end zone."""
        return self.state is DroneState.DELIVERED

    def is_in_transit(self) -> bool:
        """returns true if this drone is currently
            mid-flight on a connection"""
        return self.state is DroneState.IN_TRANSIT

    def start_transit(
        self,
        connection_key: frozenset[str],
        target_zone: str,
        turns_remaining: int,
    ) -> None:
        """Send this drone into transit toward a restricted zone.

        Args:
            connection_key: The frozenset key identifying the connection
                being traversed.
            target_zone: Name of the zone the drone will land in.
            turns_remaining: Future turns remaining after the departure turn.
                For a restricted destination, this is normally 1: the drone
                enters the connection now and arrives on the next turn.
        """

        self.current_zone = None
        self.state = DroneState.IN_TRANSIT
        self.connection_key = connection_key
        self.target_zone = target_zone
        self.turns_remaining = turns_remaining

    def advance_transit(self) -> bool:
        """Count down one turn of an in-progress transit.

        Returns:
            True if this was the final turn and the drone has now
            reached its transit_target; False if it is still flying.

        Raises:
            RuntimeError: If called while the drone isn't in transit.
        """
        if not self.is_in_transit():
            raise RuntimeError(f"{self.drone_id} is not currently in transit")

        self.turns_remaining -= 1
        return self.turns_remaining <= 0

    def arrive(self, zone_name: str, is_end_zone: bool) -> None:
        """Place this drone in a zone, ending any transit in progress.

        Args:
            zone_name: Name of the zone the drone now occupies.
            is_end_zone: Whether this zone is the map's end_hub, in
                which case the drone is considered delivered.
        """

        self.current_zone = zone_name
        self.connection_key = None
        self.target_zone = None
        self.turns_remaining = 0
        self.state = (
            DroneState.DELIVERED if is_end_zone else DroneState.WAITING
        )
