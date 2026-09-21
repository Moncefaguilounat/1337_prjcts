"""Custom exceptions raised while parsing a map file.

The subject requires that "any other parsing error must stop the
program and return a clear error message indicating the line and
cause" (VII.4). Having dedicated exception classes, instead of raising
plain strings or generic Exceptions, makes every error self-describing
and lets other code catch specific failure kinds if it ever needs to.
"""


class MapParseError(Exception):
    """Base exception for any problem found while parsing a map file.

    Every other parsing exception in this project inherits from this
    class, so calling code can catch every possible parsing failure
    with a single `except MapParseError:` if it wants to.
    """

    def __init__(self, message: str, line_number: int | None = None) -> None:
        """Initialize a MapParseError.

        Args:
            message: Human-readable description of what went wrong.
            line_number: The 1-indexed line in the map file where the
                problem was found, if known.
        """
        self.line_number = line_number
        if line_number is not None:
            message = f"Line {line_number}: {message}"
        super().__init__(message)


class InvalidMetadataError(MapParseError):
    """Raised when a [key=value ...] metadata block is malformed."""


class InvalidZoneTypeError(MapParseError):
    """Raised when a zone's `zone=` value isn't a recognized ZoneType."""


class DuplicateEntityError(MapParseError):
    """Raised when a zone name, connection, or hub is declared twice."""


class UnknownZoneError(MapParseError):
    """Raised when a connection references a zone that was never defined."""


class MissingHubError(MapParseError):
    """Raised when the map file has no start_hub or no end_hub."""
