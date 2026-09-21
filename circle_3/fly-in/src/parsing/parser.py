"""Parser for the Fly-in map file format described in the subject."""

from __future__ import annotations

from src.models.connection import Connection
from src.models.enums import ZoneType
from src.models.graph import Graph
from src.models.zone import Zone
from src.parsing.exceptions import (
    DuplicateEntityError,
    InvalidMetadataError,
    InvalidZoneTypeError,
    MapParseError,
    MissingHubError,
    UnknownZoneError,
)

_ZONE_PREFIXES = ("start_hub", "end_hub", "hub")
_ZONE_METADATA_KEYS = {"zone", "color", "max_drones"}
_CONNECTION_METADATA_KEYS = {"max_link_capacity"}


class MapParser:
    """Reads a Fly-in map file and builds a Graph plus a drone count.

    This is the only class in the project that understands the raw
    text format from the subject. Once parse() returns, every other
    part of the codebase works exclusively with typed objects (Zone,
    Connection, Graph) and never touches a raw string from the file
    again.
    """

    def parse(self, file_path: str) -> tuple[Graph, int]:
        """Parse a map file into a Graph and a drone count.

        Args:
            file_path: Path to the map file on disk.

        Returns:
            A tuple of (graph, nb_drones).

        Raises:
            MapParseError: If the file is missing, empty, or malformed
                in any way.
        """

        try:
            with open(file_path, "r", encoding="utf-8") as handle:
                raw_lines = handle.readlines()
        except OSError as error:
            raise MapParseError(
                f"Could not open map file '{file_path}': {error}"
            ) from error

        graph = Graph()
        nb_drones: int | None = None
        start_hub_count = 0
        end_hub_count = 0

        for line_number, lines in enumerate(raw_lines, start=1):
            line = self._strip_comment(lines).strip()
            if not line:
                continue

            if nb_drones is None:
                nb_drones = self._parse_nb_drones(line, line_number)
                continue

            if line.startswith("connection:"):
                connection = self._parse_connection_line(line, line_number)
                self._add_connection(graph, connection, line_number)

            elif self._is_zone_line(line):
                zone = self._parse_zone_line(line, line_number)
                if zone.is_start:
                    start_hub_count += 1
                    if start_hub_count > 1:
                        raise DuplicateEntityError(
                            "Only one 'start_hub:' zone is allowed.",
                            line_number
                        )
                if zone.is_end:
                    end_hub_count += 1
                    if end_hub_count > 1:
                        raise DuplicateEntityError(
                            "Only one 'end_hub:' zone is allowed.", line_number
                        )
                self._add_zone(graph, zone, line_number)

            else:
                raise MapParseError(f"Unrecognized line: {line}", line_number)

        if nb_drones is None:
            raise MapParseError(
                "Missing 'nb_drones:' line (file might be empty)."
            )
        self._validate_hubs(graph)
        return graph, nb_drones

    @staticmethod
    def _is_zone_line(line: str) -> bool:
        """Return whether the line has an exact supported zone prefix."""
        prefix, separator, _ = line.partition(":")
        return bool(separator) and prefix in _ZONE_PREFIXES

    @staticmethod
    def _strip_comment(raw_line: str) -> str:
        """Remove everything from '#' onward (comments)"""
        return raw_line.split('#', 1)[0]

    @staticmethod
    def _parse_nb_drones(line: str, line_number: int) -> int:
        """Parse the mandatory first line: <nb_drones>."""
        if not line.startswith("nb_drones:"):
            raise MapParseError(
                "The first line of the map must define 'nb_drones'.",
                line_number,
            )
        value = line.split(":", 1)[1].strip()
        try:
            parsed = int(value)
        except ValueError:
            parsed = -1
        if parsed <= 0:
            raise MapParseError(
                f"'nb_drones' must be a positive integer, got '{value}'.",
                line_number,
            )
        return parsed

    def _parse_zone_line(self, line: str, line_number: int) -> Zone:
        """Parse a 'start_hub:'/'end_hub:'/'hub:' line into a Zone."""
        firstpart, _, secondpart = line.partition(":")
        content, metadata_str = self._split_metadata(
            secondpart.strip(), line, line_number
        )
        parts = content.split()
        if len(parts) != 3:
            raise MapParseError(
                f"Expected '<name> <x> <y>' after '{firstpart}:', "
                f"got '{content}'.",
                line_number,
            )
        name, x_str, y_str = parts
        self._validate_zone_name(name, line_number)
        x = self._parse_int(x_str, "x coordinate", line_number)
        y = self._parse_int(y_str, "y coordinate", line_number)

        metadata = self._parse_metadata(
            metadata_str, _ZONE_METADATA_KEYS, line_number
        )
        zone_type = self._parse_zone_type(
                metadata.get("zone", "normal"),
                line_number,
        )
        max_drones = self._parse_positive_int(
                metadata.get("max_drones", "1"),
                "max_drones",
                line_number,
        )

        return Zone(
            name=name,
            x=x,
            y=y,
            zone_type=zone_type,
            color=metadata.get("color"),
            max_drones=max_drones,
            is_start=(firstpart == "start_hub"),
            is_end=(firstpart == "end_hub"),
        )

    def _parse_connection_line(
        self, line: str, line_number: int
    ) -> Connection:
        """Parse a 'connection: <zone1>-<zone2> [metadata]' line."""
        _, _, content = line.partition(":")
        firstpart, metadata_str = self._split_metadata(
                content.strip(),
                line,
                line_number,
        )
        if firstpart.count("-") != 1:
            raise MapParseError(
                f"Malformed connection '{firstpart}'. "
                "Expected '<zone1>-<zone2>'.",
                line_number,
            )
        zone_a, _, zone_b = firstpart.partition("-")
        zone_a, zone_b = zone_a.strip(), zone_b.strip()
        if not zone_a or not zone_b or " " in zone_a or " " in zone_b:
            raise MapParseError(
                f"Malformed connection '{firstpart}'.", line_number
            )
        if zone_a == zone_b:
            raise MapParseError(
                f"A zone cannot connect to itself: '{zone_a}'.", line_number
            )
        metadata = self._parse_metadata(
            metadata_str, _CONNECTION_METADATA_KEYS, line_number
        )
        max_link_capacity = self._parse_positive_int(
            metadata.get("max_link_capacity", "1"), "max_link_capacity",
            line_number,
            )
        return Connection(zone_a=zone_a, zone_b=zone_b,
                          max_link_capacity=max_link_capacity
                          )

    @staticmethod
    def _split_metadata(remainder: str, line: str, line_number: int
                        ) -> tuple[str, str]:
        """Split <content> [metadata]' into (<content>, metadata) strings."""
        if "[" not in remainder:
            if "]" in remainder:
                raise InvalidMetadataError(
                    f"Malformed metadata block on line: '{line}'.", line_number
                )
            return remainder, ""

        before, _, after = remainder.partition("[")
        if (
            remainder.count("[") != 1
            or remainder.count("]") != 1
            or not after.endswith("]")
        ):
            raise InvalidMetadataError(
                f"Malformed metadata block on line: '{line}'.", line_number
            )
        return before.strip(), after[:-1].strip()

    @staticmethod
    def _parse_metadata(
        metadata_str: str,
        allowed_keys: set[str],
        line_number: int,
    ) -> dict[str, str]:
        """Parse 'key1=value1 key2=value2' into a dict, in any order."""
        metadata: dict[str, str] = {}
        for token in metadata_str.split():
            key, separator, value = token.partition("=")
            if not key or not separator or not value:
                raise InvalidMetadataError(
                    f"Malformed metadata tag '{token}'.", line_number
                )
            if key not in allowed_keys:
                raise InvalidMetadataError(
                    f"Unsupported metadata key '{key}'.", line_number
                )
            if key in metadata:
                raise InvalidMetadataError(
                    f"Duplicate metadata key '{key}'.", line_number
                )
            metadata[key] = value
        return metadata

    @staticmethod
    def _validate_zone_name(name: str, line_number: int) -> None:
        """Reject zone names that cannot be represented in a connection."""
        if "-" in name or any(character.isspace() for character in name):
            raise MapParseError(
                f"Invalid zone name '{name}': "
                "dashes and spaces are forbidden.",
                line_number,
            )

    @staticmethod
    def _parse_zone_type(value: str, line_number: int) -> ZoneType:
        """Convert a raw 'zone=' string into a validated ZoneType."""
        try:
            return ZoneType(value)
        except ValueError:
            valid = ", ".join(zone_type.value for zone_type in ZoneType)
            raise InvalidZoneTypeError(
                f"Invalid zone type '{value}'. Must be one of: {valid}.",
                line_number,
            ) from None

    @staticmethod
    def _parse_int(value: str, field_name: str, line_number: int) -> int:
        """Parse a required integer field, raising a clear error if invalid."""
        try:
            return int(value)
        except ValueError:
            raise MapParseError(
                f"'{field_name}' must be an integer, got '{value}'.",
                line_number,
            ) from None

    @staticmethod
    def _parse_positive_int(
            value: str, field_name: str, line_number: int) -> int:
        """Parse a required positive integer field (e.g. max_drones)."""
        try:
            parsed = int(value)
        except ValueError:
            parsed = -1
        if parsed <= 0:
            raise MapParseError(
                f"'{field_name}' must be a positive integer, got '{value}'.",
                line_number,
            )
        return parsed

    @staticmethod
    def _add_zone(graph: Graph, zone: Zone, line_number: int) -> None:
        """Add a zone to the graph, raising errors in failing cases."""
        try:
            graph.add_zone(zone)
        except ValueError as error:
            raise DuplicateEntityError(str(error), line_number) from error

    @staticmethod
    def _add_connection(
        graph: Graph, connection: Connection, line_number: int
    ) -> None:
        """Add a connection to the graph, raising errors in failing cases."""
        try:
            graph.add_connection(connection)
        except ValueError as error:
            message = str(error)
            if "unknown zone" in message.lower():
                raise UnknownZoneError(message, line_number) from error
            raise DuplicateEntityError(message, line_number) from error

    @staticmethod
    def _validate_hubs(graph: Graph) -> None:
        """Ensure exactly one start_hub and one end_hub were found."""
        if graph.start_zone_name is None:
            raise MissingHubError("Map file must define a 'start_hub:' zone.")
        if graph.end_zone_name is None:
            raise MissingHubError("Map file must define an 'end_hub:' zone.")
