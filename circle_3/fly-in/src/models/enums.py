from enum import Enum


class ZoneType(Enum):
    """Supported zone types and their destination movement costs."""

    NORMAL = "normal"
    RESTRICTED = "restricted"
    PRIORITY = "priority"
    BLOCKED = "blocked"

    @property
    def move_cost(self) -> int:
        """Return the number of turns required to enter this zone type."""
        if self is ZoneType.RESTRICTED:
            return 2

        if self is ZoneType.BLOCKED:
            raise ValueError(
                "Blocked zones cannot be entered and have no movement cost."
            )
        return 1


class DroneState(Enum):
    """Possible states of a drone during the simulation."""

    WAITING = "waiting"
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
