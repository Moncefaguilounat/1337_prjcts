"""Validated input/output models and JSON file handling."""

import json
import keyword
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter
from pydantic import ValidationError, model_validator

JsonValue = str | int | float | bool | None
SUPPORTED_TYPES = {
    "boolean",
    "float",
    "integer",
    "none",
    "null",
    "number",
    "string",
}


class StrictModel(BaseModel):
    """Reject fields that are not part of a declared JSON structure."""

    model_config = ConfigDict(extra="forbid")


class ParameterSpec(BaseModel):
    """Describe one function parameter and optional finite choices."""

    model_config = ConfigDict(extra="allow")

    type: str = Field(min_length=1)
    enum: list[JsonValue] | None = None
    allowed_values: list[JsonValue] | None = None

    @model_validator(mode="after")
    def check_parameter(self) -> "ParameterSpec":
        """Normalize and validate a parameter definition."""
        self.type = self.type.strip().lower()
        if self.type not in SUPPORTED_TYPES:
            raise ValueError(f"unsupported parameter type: {self.type}")
        if self.enum is not None and self.allowed_values is not None:
            raise ValueError("use either enum or allowed_values, not both")
        if self.choices == []:
            raise ValueError("allowed values cannot be empty")
        if self.choices is not None:
            for value in self.choices:
                if not matches_type(value, self.type):
                    raise ValueError(
                        f"allowed value {value!r} does not match "
                        f"{self.type}"
                    )
        return self

    @property
    def choices(self) -> list[JsonValue] | None:
        """Return enum or allowed-values choices through one name."""
        if self.enum is not None:
            return self.enum
        return self.allowed_values


class ReturnSpec(StrictModel):
    """Describe the declared return type of a function."""

    type: str = Field(min_length=1)


class FunctionSpec(StrictModel):
    """Describe one function available to the language model."""

    name: str = Field(min_length=1)
    description: str = Field(min_length=1)
    parameters: dict[str, ParameterSpec]
    returns: ReturnSpec

    @model_validator(mode="after")
    def check_names(self) -> "FunctionSpec":
        """Require unambiguous function and parameter identifiers."""
        if not self.name.isidentifier() or keyword.iskeyword(self.name):
            raise ValueError(f"invalid function name: {self.name!r}")
        for name in self.parameters:
            if not name.isidentifier() or keyword.iskeyword(name):
                raise ValueError(f"invalid parameter name: {name!r}")
        return self


class Request(StrictModel):
    """Contain one natural-language request from the input file."""

    prompt: str


class FunctionCall(StrictModel):
    """Represent exactly one required output object."""

    prompt: str
    name: str
    parameters: dict[str, JsonValue]


class Settings(StrictModel):
    """Contain validated command-line paths and generation settings."""

    functions_path: Path
    input_path: Path
    output_path: Path
    model_name: str = "Qwen/Qwen3-0.6B"
    max_tokens: int = Field(default=96, ge=1, le=512)
    visualize: bool = False


def matches_type(value: Any, declared: str) -> bool:
    """Return whether a Python value strictly matches a schema type."""
    kind = declared.lower()
    if kind in {"number", "float"}:
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if kind == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if kind == "string":
        return isinstance(value, str)
    if kind == "boolean":
        return isinstance(value, bool)
    if kind in {"none", "null"}:
        return value is None
    return False


def _read_json_array(path: Path) -> list[Any]:
    """Read one JSON array and report file errors with context."""
    try:
        with path.open("r", encoding="utf-8") as stream:
            value = json.load(stream)
    except FileNotFoundError as error:
        raise ValueError(f"input file not found: {path}") from error
    except PermissionError as error:
        raise ValueError(f"cannot read input file: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(
            f"invalid JSON in {path} at line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error
    except OSError as error:
        raise ValueError(f"cannot read {path}: {error}") from error
    if not isinstance(value, list):
        raise ValueError(f"expected a JSON array in {path}")
    return value


def load_functions(path: Path) -> list[FunctionSpec]:
    """Read and validate all available function definitions."""
    try:
        functions = TypeAdapter(list[FunctionSpec]).validate_python(
            _read_json_array(path)
        )
    except ValidationError as error:
        raise ValueError(f"invalid function definitions in {path}: {error}") \
            from error
    if not functions:
        raise ValueError("at least one function definition is required")
    names = [function.name for function in functions]
    if len(names) != len(set(names)):
        raise ValueError("function names must be unique")
    if "fn_none" in names:
        raise ValueError("fn_none is reserved for unmatched requests")
    return functions


def load_requests(path: Path) -> list[Request]:
    """Read and validate all natural-language requests."""
    try:
        return TypeAdapter(list[Request]).validate_python(
            _read_json_array(path)
        )
    except ValidationError as error:
        raise ValueError(f"invalid prompts in {path}: {error}") from error


def write_calls(path: Path, calls: list[FunctionCall]) -> None:
    """Write exact output objects through a temporary JSON file."""
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".tmp")
        payload = [call.model_dump() for call in calls]
        with temporary.open("w", encoding="utf-8") as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
        temporary.replace(path)
    except OSError as error:
        raise ValueError(f"cannot write output file {path}: {error}") \
            from error
