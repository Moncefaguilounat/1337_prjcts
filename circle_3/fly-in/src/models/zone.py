"""The Zone model: a single node in the drone network."""
from __future__ import annotations

from src.models.enums import ZoneType


class Zone:
    """A single zone (station) in the map.

    A Zone only knows about itself: its identity, its type, and who is
    currently standing inside it. It knows nothing about connections
    to other zones, and nothing about pathfinding or turns — that
    logic belongs to other classes (Connection, Graph, Simulator).

    Attributes:
        name: Unique identifier for this zone (e.g. "roof1").
        x: X coordinate, used only for visualization.
        y: Y coordinate, used only for visualization.
        zone_type: One of the four ZoneType values.
        color: Optional color string, used only for visualization.
        max_drones: How many drones may occupy this zone at once.
        is_start: True if this is the unique start_hub.
        is_end: True if this is the unique end_hub.
        occupants: Set of drone IDs currently inside this zone.
    """
    def __init__(
        self,
        name: str,
        x: int,
        y: int,
        zone_type: ZoneType = ZoneType.NORMAL,
        color: str | None = None,
        max_drones: int = 1,
        is_start: bool = False,
        is_end: bool = False,
    ) -> None:
        """Initialize a zone.

        Args:
            name: Unique zone name.
            x: X coordinate.
            y: Y coordinate.
            zone_type: The zone's type (defaults to normal).
            color: Optional display color.
            max_drones: Capacity of the zone (defaults to 1).
            is_start: Whether this zone is the start_hub.
            is_end: Whether this zone is the end_hub.
        """
        self.name = name
        self.x = x
        self.y = y
        self.zone_type = zone_type
        self.color = color
        self.max_drones = max_drones
        self.is_start = is_start
        self.is_end = is_end
        self.occupants: set[str] = set()

    def is_blocked(self) -> bool:
        """Return True if drones are forbidden from ever entering this zone."""
        return self.zone_type is ZoneType.BLOCKED

    def has_capacity(self) -> bool:
        """Return True if at least one more drone
            could enter this zone right now.

        The start and end zones are exempt from capacity limits
        """
        if self.is_start or self.is_end:
            return True
        return len(self.occupants) < self.max_drones

    def add_drone(self, drone_id: str) -> None:
        """Register a drone as being physically inside this zone.

        Raises:
            RuntimeError: If the zone has no free capacity. This should never
            trigger if the simulator checks has_capacity() before , therefore
            its just a deffensive programming

        """
        if not self.has_capacity():
            raise RuntimeError(f"Zone '{self.name}' is at full capacity")
        self.occupants.add(drone_id)

    def remove_drone(self, drone_id: str) -> None:
        """Removes a drone from being physically inside this zone"""
        self.occupants.discard(drone_id)

    def move_cost(self) -> int:
        """Returns the move cost that this zone type requires"""
        return self.zone_type.move_cost
