"""Select a function, then complete its call one argument at a time."""

import json
import sys

from pydantic import BaseModel, ConfigDict

from .data import (
    FunctionCall,
    FunctionSpec,
    JsonValue,
    ParameterSpec,
    Request,
    matches_type,
)
from .decoder import TokenGenerator


class FunctionCaller(BaseModel):
    """Own the order of LLM requests, not the token-selection mechanics."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    functions: list[FunctionSpec]
    generator: TokenGenerator

    def call(self, request: Request) -> FunctionCall | None:
        selected = self.generator.choose(
            self._selection_prompt(request.prompt),
            {function.name: function.name for function in self.functions}
            | {"fn_none": "fn_none"},
        )
        if selected == "fn_none":
            return None
        function = next(
            (item for item in self.functions if item.name == selected),
            None,
        )
        if function is None:
            raise ValueError(f"selected unknown function {selected!r}")

        arguments: dict[str, JsonValue] = {}
        for name, specification in function.parameters.items():
            try:
                arguments[name] = self._argument(
                    request.prompt, function, name, specification, arguments
                )
            except (ValueError, TypeError) as error:
                print(
                    f"Warning: {function.name}.{name}: {error}; "
                    "using a schema-compatible fallback",
                    file=sys.stderr,
                )
                arguments[name] = self._fallback(specification)
        self._validate(function, arguments)
        return FunctionCall(
            prompt=request.prompt,
            name=function.name,
            parameters=arguments,
        )

    def _argument(
        self,
        request: str,
        function: FunctionSpec,
        name: str,
        specification: ParameterSpec,
        earlier: dict[str, JsonValue],
    ) -> JsonValue:
        if specification.choices is not None:
            values = {
                str(index): value
                for index, value in enumerate(specification.choices)
            }
            return self._literal(request, function.name, name, earlier, values)

        kind = specification.type
        if kind in {"number", "float", "integer"}:
            prompt = self._completion_prompt(
                request, function.name, name, earlier, numeric=True
            )
            return self.generator.number(prompt, kind == "integer")
        if kind == "string":
            prompt = self._completion_prompt(
                request, function.name, name, earlier, numeric=False
            )
            return self.generator.string(prompt)
        if kind == "boolean":
            return self._literal(
                request, function.name, name, earlier,
                {"true": True, "false": False},
            )
        if kind in {"none", "null"}:
            return self._literal(
                request, function.name, name, earlier, {"null": None}
            )
        raise ValueError(f"unsupported type {kind!r}")

    def _literal(
        self,
        request: str,
        function: str,
        name: str,
        earlier: dict[str, JsonValue],
        values: dict[str, JsonValue],
    ) -> JsonValue:
        prompt = self._completion_prompt(
            request, function, name, earlier, numeric=True
        )
        options = {
            label: json.dumps(value, ensure_ascii=False)
            for label, value in values.items()
        }
        label = self.generator.choose(prompt, options)
        return values[label]

    def _selection_prompt(self, request: str) -> str:
       ## """Present the registry in the friend's selector prompt style."""
        registry = {
            function.name: function.description
            for function in self.functions
        }
        registry["fn_none"] = (
            "Fallback function. Select this only when none of the available "
            "functions can reasonably fulfill the user's intent. Do not "
            "choose this merely because the wording differs or the input "
            "values are different. Use fn_none only if no function is an "
            "appropriate match."
        )
        return "\n".join([
            "<|im_start|>system",
            "        You are a function selector. Determine the single "
            "best function for the user's request.",
            " ",
            "        Registered functions:",
            f"        {json.dumps(registry, indent=2)}",
            " ",
            "        Instructions:",
            "        - Choose exactly one function from the list above.",
            "        - If none of the functions accurately matches the "
            "request, return fn_none.",
            "        - Do not infer unsupported functionality.",
            "        - Respond with only the function name.",
            " ",
            "        Examples:",
            '        Request: "Calculate 2 + 3" → fn_add_numbers',
            '        Request: "Subtract 3 from 5" → fn_subtract_numbers',
            '        Request: "Show me the weather in Paris" → fn_get_weather',
            '        Request: "Reverse \'abc\'" → fn_reverse_string',
            '        Request: "Multiply 4 by 5" → fn_none',
            '        Request: "Make \'hello\' uppercase" → fn_none',
            '        Request: "Tell me something funny" → fn_none',
            " ",
            "        Output exactly one function name and nothing else."
            "<|im_end|>",
            "        <|im_start|>user",
            f"        Request: {request}<|im_end|>",
            "        <|im_start|>assistant",
            "        ",
        ])

    @staticmethod
    def _prior(earlier: dict[str, JsonValue]) -> str:
        pieces = []
        for name, value in earlier.items():
            if isinstance(value, str):
                pieces.append(f'{name}="{value}", ')
            else:
                pieces.append(f"{name}={value},\n")
        return "".join(pieces)

    @classmethod
    def _completion_prompt(
        cls,
        request: str,
        function: str,
        name: str,
        earlier: dict[str, JsonValue],
        numeric: bool,
    ) -> str:
        previous = cls._prior(earlier)
        if numeric:
            return f"\n        #-> {request}\n{function}({previous}{name}="
        return f'\n-> {request}\n{function}({previous}{name}="'

    @staticmethod
    def _fallback(specification: ParameterSpec) -> JsonValue:
        if specification.choices is not None:
            return specification.choices[0]
        if specification.type in {"number", "float"}:
            return 0.0
        if specification.type == "integer":
            return 0
        if specification.type == "boolean":
            return False
        if specification.type in {"none", "null"}:
            return None
        return ""

    @staticmethod
    def _validate(
        function: FunctionSpec,
        arguments: dict[str, JsonValue],
    ) -> None:
        if set(arguments) != set(function.parameters):
            raise ValueError("arguments do not match the function schema")
        for name, specification in function.parameters.items():
            value = arguments[name]
            if not matches_type(value, specification.type):
                raise ValueError(
                    f"{name!r} does not match {specification.type}"
                )
            if specification.choices is not None \
                    and value not in specification.choices:
                raise ValueError(f"{name!r} is outside its allowed values")
