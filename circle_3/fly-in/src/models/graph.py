"""The Graph model: the full network of zones and connections."""

from src.models.connection import Connection
from src.models.zone import Zone


class Graph:
    """The complete drone network built by the parser.

    The Graph owns every Zone and Connection and provides the lookups
    that the pathfinder and simulator need: "who are this zone's
    neighbors", "what connection links these two zones", and so on.

    Attributes:
        zones: Maps zone name to Zone object.
        connections: Maps a connection's frozenset key to Connection object.
        start_zone_name: Name of the unique start_hub zone.
        end_zone_name: Name of the unique end_hub zone.
    """

    def __init__(self) -> None:
        """Initialize an empty Graph."""
        self.zones: dict[str, Zone] = {}
        self.connections: dict[frozenset[str], Connection] = {}
        self._adjacency: dict[str, list[str]] = {}
        self.start_zone_name: str | None = None
        self.end_zone_name: str | None = None

    def add_zone(self, zone: Zone) -> None:
        """Register a new zone in the graph.

        Args:
            zone: The Zone to add.

        Raises:
            ValueError: If a zone with the same name already exists.
        """
        if zone.name in self.zones:
            raise ValueError(f"Duplicate zone name: '{zone.name}'.")
        self.zones[zone.name] = zone
        self._adjacency[zone.name] = []
        if zone.is_start:
            self.start_zone_name = zone.name
        if zone.is_end:
            self.end_zone_name = zone.name

    def add_connection(self, connection: Connection) -> None:
        """Register a new connection in the graph.

        Args:
            connection: The Connection to add.

        Raises:
            ValueError: If either endpoint zone doesn't exist yet, or
                if this connection (in either direction) already exists.
        """
        if connection.zone_a == connection.zone_b:
            raise ValueError(
                f"A zone cannot connect to itself: '{connection.zone_a}'."
            )
        for zone_name in (connection.zone_a, connection.zone_b):
            if zone_name not in self.zones:
                raise ValueError(
                    f"Connection references unknown zone '{zone_name}'."
                )

        key = connection.key()
        if key in self.connections:
            raise ValueError(
                f"Duplicate connection between '{connection.zone_a}' and "
                f"'{connection.zone_b}'."
            )

        self.connections[key] = connection
        self._adjacency[connection.zone_a].append(connection.zone_b)
        self._adjacency[connection.zone_b].append(connection.zone_a)

    def neighbors(self, zone_name: str) -> list[str]:
        """Return the names of zones directly reachable from the given zone.

        Args:
            zone_name: The zone to look up.

        Returns:
            A list of neighboring zone names (empty if none, or if the
            zone name is unknown).
        """
        return list(self._adjacency.get(zone_name, []))

    def get_zone(self, zone_name: str) -> Zone:
        """Return the Zone object for a given name.

        Raises:
            KeyError: If no zone with that name exists.
        """
        return self.zones[zone_name]

    def get_connection(self, zone_a: str, zone_b: str) -> Connection:
        """Return the Connection object linking two zones.

        Args:
            zone_a: One endpoint's name.
            zone_b: The other endpoint's name.

        Raises:
            ValueError: If no connection exists between these two zones.
        """
        key = frozenset({zone_a, zone_b})
        if key not in self.connections:
            raise ValueError(f"No connection between '{zone_a}' "
                             f"and '{zone_b}'.")
        return self.connections[key]
