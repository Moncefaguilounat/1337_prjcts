"""ANSI color helpers for the dependency-free terminal visualizer."""

from __future__ import annotations


RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

COLOR_CODES: dict[str, str] = {
    "green": "\033[92m",
    "yellow": "\033[93m",
    "red": "\033[91m",
    "blue": "\033[94m",
    "gray": "\033[90m",
    "purple": "\033[95m",
    "brown": "\033[38;5;130m",
}
COLOR_NAMES = tuple(COLOR_CODES)

_ALIASES = {
    "black": "gray",
    "crimson": "red",
    "darkred": "red",
    "gold": "yellow",
    "maroon": "red",
    "orange": "yellow",
    "rainbow": "blue",
    "violet": "purple",
}


def resolve_color_name(color_name: str | None) -> str | None:
    """Map arbitrary color metadata into the seven terminal colors."""
    if color_name is None:
        return None

    normalized = color_name.lower()
    normalized = _ALIASES.get(normalized, normalized)
    if normalized in COLOR_CODES:
        return normalized

    stable_number = sum(
        (index + 1) * ord(character)
        for index, character in enumerate(normalized)
    )
    return COLOR_NAMES[stable_number % len(COLOR_NAMES)]


def style_text(
    text: str,
    color_name: str | None = None,
    *,
    bold: bool = False,
    dim: bool = False,
    enabled: bool = True,
) -> str:
    """Wrap text in ANSI styling when terminal colors are enabled."""
    if not enabled:
        return text

    codes = BOLD if bold else ""
    codes += DIM if dim else ""
    resolved_name = resolve_color_name(color_name)
    if resolved_name is not None:
        codes += COLOR_CODES[resolved_name]
    return f"{codes}{text}{RESET}" if codes else text
