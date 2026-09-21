"""Command-line entry point for ``python -m src``."""

import argparse
from pathlib import Path
import sys
import time

from pydantic import ValidationError

from .caller import FunctionCaller
from .data import (
    FunctionCall,
    Settings,
    load_functions,
    load_requests,
    write_calls,
)
from .decoder import TokenGenerator
from .llm import LanguageModel


def parse_arguments(values: list[str] | None = None) -> argparse.Namespace:
    """Read paths and options supplied on the command line."""
    parser = argparse.ArgumentParser(
        description="Generate function calls with token masks."
    )
    parser.add_argument(
        "--functions_definition",
        default="data/input/functions_definition.json",
    )
    parser.add_argument(
        "--input",
        default="data/input/function_calling_tests.json",
    )
    parser.add_argument(
        "--output",
        default="data/output/function_calling_results.json",
    )
    parser.add_argument("--visualize", action="store_true")
    parser.add_argument("--max-tokens", type=int, default=50)
    return parser.parse_args(values)


def run(
    settings: Settings,
    model: LanguageModel | None = None,
) -> tuple[list[FunctionCall], list[str]]:
    """Process every request and write all successful function calls."""
    functions = load_functions(settings.functions_path)
    requests = load_requests(settings.input_path)

    if model is None:
        print(f"Loading model {settings.model_name}...")
        model = LanguageModel.load(settings.model_name)

    generator = TokenGenerator(
        model=model,
        max_tokens=settings.max_tokens,
        visualize=settings.visualize,
    )
    caller = FunctionCaller(functions=functions, generator=generator)
    calls: list[FunctionCall] = []
    warnings: list[str] = []

    started = time.monotonic()
    for index, request in enumerate(requests, start=1):
        try:
            call = caller.call(request)
            if call is None:
                warnings.append(
                    f"prompt {index} matched no registered function"
                )
            else:
                calls.append(call)
        except Exception as error:
            warnings.append(f"prompt {index} failed: {error}")

    write_calls(settings.output_path, calls)
    elapsed = time.monotonic() - started
    for warning in warnings:
        print(f"Warning: {warning}", file=sys.stderr)
    print(
        f"Wrote {len(calls)} calls to {settings.output_path} "
        f"in {elapsed:.2f}s"
    )
    return calls, warnings


def main(values: list[str] | None = None) -> int:
    """Build validated settings and turn failures into readable messages."""
    arguments = parse_arguments(values)
    try:
        settings = Settings(
            functions_path=Path(arguments.functions_definition),
            input_path=Path(arguments.input),
            output_path=Path(arguments.output),
            max_tokens=arguments.max_tokens,
            visualize=arguments.visualize,
        )
        run(settings)
    except (ValueError, ValidationError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Error: interrupted by user", file=sys.stderr)
        return 130
    except Exception as error:
        print(
            f"Error: unexpected {type(error).__name__}: {error}",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
