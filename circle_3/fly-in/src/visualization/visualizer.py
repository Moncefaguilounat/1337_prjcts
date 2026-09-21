"""Clear, animated ANSI terminal visualization for Fly-in."""

from __future__ import annotations

from dataclasses import dataclass
import shutil
import sys
import time
from typing import TextIO

from src.models.graph import Graph
from src.models.zone import Zone
from src.visualization.theme import COLOR_NAMES, resolve_color_name, style_text


_RESET_SCREEN = "\033[H\033[2J"
_HIDE_CURSOR = "\033[?25l"
_SHOW_CURSOR = "\033[?25h"


class VisualizationError(RuntimeError):
    """Raised when a movement history cannot be shown safely."""


@dataclass
class _CanvasCell:
    """One visible character in the terminal graph canvas."""

    character: str = " "
    color_name: str | None = None
    bold: bool = False
    is_node: bool = False


class TerminalVisualizer:
    """Replay simulator turns while keeping every zone marker fixed."""

    def __init__(
        self,
        graph: Graph,
        nb_drones: int,
        delay_seconds: float = 1.0,
        stream: TextIO | None = None,
        use_color: bool | None = None,
    ) -> None:
        """Prepare a dependency-free terminal replay.

        Args:
            graph: Parsed graph whose coordinates and metadata are displayed.
            nb_drones: Number of drones that begin at the start zone.
            delay_seconds: Pause between two consecutive simulation turns.
            stream: Output stream, normally standard output.
            use_color: Optional ANSI-color override, mainly used by tests.

        Raises:
            VisualizationError: If the graph or replay delay is invalid.
        """
        if graph.start_zone_name is None or graph.end_zone_name is None:
            raise VisualizationError(
                "The visualizer requires unique start and end zones."
            )
        if nb_drones <= 0:
            raise VisualizationError(
                "The visualizer requires at least one drone."
            )
        if delay_seconds < 0:
            raise VisualizationError(
                "The visualization delay cannot be negative."
            )

        uses_default_stream = stream is None
        self.graph = graph
        self.nb_drones = nb_drones
        self.delay_seconds = delay_seconds
        self.stream = stream if stream is not None else sys.stdout
        self._interactive = bool(
            getattr(self.stream, "isatty", lambda: False)()
        )
        # Some WSL launchers report stdout as non-interactive even though they
        # display ANSI controls. Normal visual runs must still replace frames.
        self._screen_control = uses_default_stream or self._interactive
        self._use_color = (
            self._screen_control if use_color is None else use_color
        )
        self._positions: dict[str, str | None] = {
            f"D{number}": graph.start_zone_name
            for number in range(1, nb_drones + 1)
        }
        self._transit_edges: dict[str, frozenset[str]] = {}

    def animate(self, history: list[list[str]]) -> None:
        """Apply, render, and pause after every recorded simulation turn."""
        if not history:
            raise VisualizationError("The simulation history is empty.")

        if self._screen_control:
            self.stream.write(_HIDE_CURSOR)

        try:
            total_turns = len(history)
            for turn_number, movements in enumerate(history, start=1):
                active_edges = self._apply_turn(movements)
                self.stream.write(
                    self._render_frame(
                        turn_number,
                        total_turns,
                        movements,
                        active_edges,
                    )
                )
                self.stream.flush()
                if turn_number < total_turns and self.delay_seconds > 0:
                    time.sleep(self.delay_seconds)
        finally:
            if self._screen_control:
                self.stream.write(_SHOW_CURSOR)
                self.stream.flush()

    def _apply_turn(self, movements: list[str]) -> set[frozenset[str]]:
        """Apply one turn and return the connections used in that turn."""
        active_edges: set[frozenset[str]] = set()
        moved_drones: set[str] = set()

        for movement in movements:
            parts = movement.split("-")
            if len(parts) not in (2, 3):
                raise VisualizationError(
                    f"Malformed movement token '{movement}'."
                )

            drone_id = parts[0]
            destination_name = parts[-1]
            if drone_id not in self._positions:
                raise VisualizationError(
                    f"Movement references unknown drone '{drone_id}'."
                )
            if drone_id in moved_drones:
                raise VisualizationError(
                    f"Drone '{drone_id}' moves twice in one turn."
                )
            if destination_name not in self.graph.zones:
                raise VisualizationError(
                    f"Movement references unknown zone "
                    f"'{destination_name}'."
                )
            moved_drones.add(drone_id)

            if len(parts) == 3:
                source_name = parts[1]
                if self._positions[drone_id] != source_name:
                    raise VisualizationError(
                        f"Restricted movement for '{drone_id}' has a "
                        "wrong source."
                    )
                edge = frozenset({source_name, destination_name})
                self._validate_edge(edge)
                self._positions[drone_id] = None
                self._transit_edges[drone_id] = edge
            elif self._positions[drone_id] is None:
                edge = self._finish_transit(drone_id, destination_name)
                self._positions[drone_id] = destination_name
            else:
                current_zone = self._positions[drone_id]
                if current_zone is None:
                    raise VisualizationError(
                        f"Drone '{drone_id}' has no source zone."
                    )
                edge = frozenset({current_zone, destination_name})
                self._validate_edge(edge)
                self._positions[drone_id] = destination_name

            active_edges.add(edge)

        return active_edges

    def _finish_transit(
        self, drone_id: str, destination_name: str
    ) -> frozenset[str]:
        """Validate and finish a restricted-zone arrival."""
        edge = self._transit_edges.pop(drone_id, None)
        if edge is None or destination_name not in edge:
            raise VisualizationError(
                f"Drone '{drone_id}' has an invalid restricted arrival."
            )
        return edge

    def _validate_edge(self, edge: frozenset[str]) -> None:
        """Ensure a visualized movement uses a real graph connection."""
        if edge not in self.graph.connections:
            endpoints = "-".join(sorted(edge))
            raise VisualizationError(
                f"Movement uses missing connection '{endpoints}'."
            )

    def _render_frame(
        self,
        turn_number: int,
        total_turns: int,
        movements: list[str],
        active_edges: set[frozenset[str]],
    ) -> str:
        """Build one complete frame without changing simulation state."""
        terminal = shutil.get_terminal_size(fallback=(110, 34))
        width = max(44, min(terminal.columns, 120))
        delivered = self._delivered_count()
        movement_lines = self._movement_lines(movements, width)
        final_line_count = 1 if turn_number == total_turns else 0
        reserved_lines = 10 + len(movement_lines) + final_line_count
        graph_height = self._graph_height(
            terminal.lines, reserved_lines
        )

        frame: list[str] = []
        frame.extend(
            [
                "=" * width,
                self._style(
                    "FLY-IN TERMINAL VISUALIZER".center(width),
                    "blue",
                    bold=True,
                ),
                "=" * width,
                (
                    f"Turn {turn_number}/{total_turns}  |  "
                    f"Delivered {delivered}/{self.nb_drones}  |  "
                    f"Zones {len(self.graph.zones)}  |  "
                    f"Connections {len(self.graph.connections)}"
                ),
                self._progress_line(delivered, width),
            ]
        )
        frame.extend(self._graph_lines(width, graph_height, active_edges))
        frame.extend(self._symbol_legend_lines())
        frame.append(self._color_legend())
        frame.extend(movement_lines)

        if turn_number == total_turns:
            turn_word = "turn" if total_turns == 1 else "turns"
            frame.append(
                self._style(
                    f"Simulation complete in {total_turns} {turn_word}.",
                    "green",
                    bold=True,
                )
            )

        rendered = "\n".join(frame) + "\n"
        if self._screen_control:
            return _RESET_SCREEN + rendered
        return rendered

    def _graph_height(
        self, terminal_lines: int, reserved_lines: int
    ) -> int:
        """Keep the complete frame within the current terminal height."""
        y_values = [zone.y for zone in self.graph.zones.values()]
        coordinate_height = (max(y_values) - min(y_values)) * 2 + 3
        available_height = max(5, terminal_lines - reserved_lines)
        return min(18, max(5, min(coordinate_height, available_height)))

    def _graph_lines(
        self,
        width: int,
        height: int,
        active_edges: set[frozenset[str]],
    ) -> list[str]:
        """Draw connections first, then compact zone states above them."""
        canvas_width = width - 2
        canvas = [
            [_CanvasCell() for _ in range(canvas_width)]
            for _ in range(height)
        ]
        coordinates = self._scaled_coordinates(canvas_width, height)

        for connection in self.graph.connections.values():
            edge = connection.key()
            self._draw_connection(
                canvas,
                coordinates[connection.zone_a],
                coordinates[connection.zone_b],
                edge in active_edges,
            )

        zone_counts = self._zone_counts()
        for zone_name, zone in self.graph.zones.items():
            x, y = coordinates[zone_name]
            cell = canvas[y][x]
            character = self._zone_character(
                zone, zone_counts[zone_name]
            )
            if cell.is_node:
                character = "@"
            canvas[y][x] = _CanvasCell(
                character=character,
                color_name=resolve_color_name(zone.color),
                bold=True,
                is_node=True,
            )

        border = "+" + "-" * canvas_width + "+"
        lines = [border]
        for row in canvas:
            rendered = "".join(self._render_cell(cell) for cell in row)
            lines.append("|" + rendered + "|")
        lines.append(border)
        return lines

    def _scaled_coordinates(
        self, width: int, height: int
    ) -> dict[str, tuple[int, int]]:
        """Scale arbitrary map coordinates into the compact canvas."""
        x_values = [zone.x for zone in self.graph.zones.values()]
        y_values = [zone.y for zone in self.graph.zones.values()]
        min_x, max_x = min(x_values), max(x_values)
        min_y, max_y = min(y_values), max(y_values)
        coordinates: dict[str, tuple[int, int]] = {}

        for zone_name, zone in self.graph.zones.items():
            x = self._scale(
                zone.x, min_x, max_x, 1, width - 2
            )
            scaled_y = self._scale(zone.y, min_y, max_y, 1, height - 2)
            coordinates[zone_name] = (x, height - 1 - scaled_y)

        return coordinates

    @staticmethod
    def _scale(
        value: int,
        minimum: int,
        maximum: int,
        output_minimum: int,
        output_maximum: int,
    ) -> int:
        """Scale one coordinate, centering an axis with no range."""
        if minimum == maximum:
            return (output_minimum + output_maximum) // 2
        ratio = (value - minimum) / (maximum - minimum)
        return round(
            output_minimum
            + ratio * (output_maximum - output_minimum)
        )

    @staticmethod
    def _draw_connection(
        canvas: list[list[_CanvasCell]],
        start: tuple[int, int],
        end: tuple[int, int],
        is_active: bool,
    ) -> None:
        """Draw one horizontal, vertical, or diagonal graph connection."""
        start_x, start_y = start
        end_x, end_y = end
        delta_x = end_x - start_x
        delta_y = end_y - start_y
        steps = max(abs(delta_x), abs(delta_y))
        if steps <= 1:
            return

        character = "-" if delta_y == 0 else "|" if delta_x == 0 else "."
        color_name = "blue" if is_active else "gray"
        for step in range(1, steps):
            x = round(start_x + delta_x * step / steps)
            y = round(start_y + delta_y * step / steps)
            cell = canvas[y][x]
            if cell.character == " ":
                cell.character = character
            elif cell.character != character and not cell.is_node:
                cell.character = "+"
            if is_active or cell.color_name is None:
                cell.color_name = color_name
                cell.bold = is_active

    @staticmethod
    def _zone_character(zone: Zone, drone_count: int) -> str:
        """Show a zone state, replacing it with occupancy when needed."""
        if drone_count > 9:
            return "*"
        if drone_count > 0:
            return str(drone_count)
        if zone.is_start:
            return "S"
        if zone.is_end:
            return "E"
        if zone.is_blocked():
            return "X"
        marker_by_type = {
            "restricted": "R",
            "priority": "P",
            "normal": "o",
        }
        return marker_by_type[zone.zone_type.value]

    def _zone_counts(self) -> dict[str, int]:
        """Count visible drones at every zone for the current turn."""
        counts = {zone_name: 0 for zone_name in self.graph.zones}
        for zone_name in self._positions.values():
            if zone_name is not None:
                counts[zone_name] += 1
        return counts

    @staticmethod
    def _symbol_legend_lines() -> list[str]:
        """Explain the compact zone-state symbols."""
        return [
            "Symbols: S=start  E=end  o=normal  P=priority",
            "         R=restricted  X=blocked  1-9/*=drones  @=overlap",
        ]

    def _movement_lines(
        self, movements: list[str], width: int
    ) -> list[str]:
        """Wrap and color the current turn's exact movement tokens."""
        prefix = "MOVEMENTS: "
        continuation = " " * len(prefix)
        if not movements:
            return [prefix + "none"]

        lines: list[str] = []
        current_raw: list[str] = []
        current_length = len(prefix)
        for movement in movements:
            added = len(movement) + (1 if current_raw else 0)
            if current_raw and current_length + added > width:
                lines.append(
                    self._styled_movement_line(
                        prefix if not lines else continuation,
                        current_raw,
                    )
                )
                current_raw = []
                current_length = len(continuation)
            current_raw.append(movement)
            separator_length = 1 if len(current_raw) > 1 else 0
            current_length += len(movement) + separator_length
        lines.append(
            self._styled_movement_line(
                prefix if not lines else continuation,
                current_raw,
            )
        )
        return lines

    def _styled_movement_line(
        self, prefix: str, movements: list[str]
    ) -> str:
        """Color movement tokens by their destination metadata."""
        styled = []
        for movement in movements:
            destination = self.graph.get_zone(movement.split("-")[-1])
            styled.append(
                self._style(
                    movement,
                    resolve_color_name(destination.color),
                    bold=True,
                )
            )
        return prefix + " ".join(styled)

    def _progress_line(self, delivered: int, width: int) -> str:
        """Render delivered progress with a compact bar."""
        bar_width = max(12, min(32, width - 38))
        completed = round(bar_width * delivered / self.nb_drones)
        bar = "#" * completed + "-" * (bar_width - completed)
        percentage = round(100 * delivered / self.nb_drones)
        return (
            f"Progress [{bar}] {percentage}%"
        )

    def _color_legend(self) -> str:
        """Show the intentionally small seven-color palette."""
        names = [
            self._style(name, name, bold=True) for name in COLOR_NAMES
        ]
        return "COLORS: " + "  ".join(names)

    def _delivered_count(self) -> int:
        """Count drones whose visible position is the end zone."""
        return sum(
            zone_name == self.graph.end_zone_name
            for zone_name in self._positions.values()
        )

    def _render_cell(self, cell: _CanvasCell) -> str:
        """Render one canvas character with its optional ANSI styling."""
        return self._style(
            cell.character,
            cell.color_name,
            bold=cell.bold,
            dim=not cell.bold and cell.character != " ",
        )

    def _style(
        self,
        text: str,
        color_name: str | None = None,
        *,
        bold: bool = False,
        dim: bool = False,
    ) -> str:
        """Apply ANSI styling according to the output stream capability."""
        return style_text(
            text,
            color_name,
            bold=bold,
            dim=dim,
            enabled=self._use_color,
        )
