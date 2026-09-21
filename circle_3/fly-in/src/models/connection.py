"""The Connection model: an edge linking two zones."""


class Connection:
    """A bidirectional link between two zones.

    Like Zone, a Connection only manages its own state: which two
    zones it links, its traversal capacity, and who is currently
    traveling on it. It doesn't know about the wider graph.

    Attributes:
        zone_a: Name of one endpoint zone.
        zone_b: Name of the other endpoint zone.
        max_link_capacity: How many drones may traverse this
            connection simultaneously.
        occupants: Set of drone IDs currently traversing this
            connection (relevant for multi-turn restricted movement).
    """
    def __init__(
        self,
        zone_a: str,
        zone_b: str,
        max_link_capacity: int = 1,
    ) -> None:
        self.zone_a = zone_a
        self.zone_b = zone_b
        self.max_link_capacity = max_link_capacity
        self.occupants: set[str] = set()

    def other_end(self, zone_name: str) -> str:
        """Given one endpoint, return the other endpoint's name.

        Args:
            zone_name: One of the two zone names on this connection.

        Returns:
            The name of the opposite zone.

        Raises:
            ValueError: If zone_name is not part of this connection.
        """
        if zone_name == self.zone_a:
            return self.zone_b
        if zone_name == self.zone_b:
            return self.zone_a
        raise ValueError(f"{zone_name} is not an endpoint of this connection")

    def has_capacity(self) -> bool:
        """return true if at least one drone can go through this connection"""
        return len(self.occupants) < self.max_link_capacity

    def enter(self, drone_id: str) -> None:
        """Register a drone as currently traversing this connection.

        Raises:
            RuntimeError: If the connection has no free capacity.
        """
        if not self.has_capacity():
            raise RuntimeError(
                f"Connection '{self.zone_a}-{self.zone_b}' is at full capacit"
                f"y ({self.max_link_capacity})."
            )
        self.occupants.add(drone_id)

    def leave(self, drone_id: str) -> None:
        """removes drone from this connection (arrived or left)"""
        self.occupants.discard(drone_id)

    def key(self) -> frozenset[str]:
        """Return a hashable, order-independent identifier for this connection.

        Since connections are bidirectional, "a-b" and "b-a" must be
        treated as the same connection. A frozenset of the two names
        does exactly that: frozenset({"a", "b"}) == frozenset({"b", "a"}).
        """
        return frozenset({self.zone_a, self.zone_b})
