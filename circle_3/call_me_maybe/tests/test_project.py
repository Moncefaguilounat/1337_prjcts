"""Tests of the simple encode/decode generation path."""

import json
from pathlib import Path
import tempfile
import unittest

from src.__main__ import run
from src.caller import FunctionCaller
from src.data import (
    FunctionCall,
    FunctionSpec,
    Request,
    Settings,
    load_functions,
    load_requests,
    write_calls,
)
from src.decoder import TokenGenerator
from src.llm import LanguageModel
from tests.fakes import ScriptedModel


def make_model(*answers: str, invalid_id: int = 255) -> LanguageModel:
    return LanguageModel.from_backend(
        ScriptedModel.from_texts(*answers, invalid_id=invalid_id)
    )


def greet_spec() -> FunctionSpec:
    return FunctionSpec.model_validate({
        "name": "fn_greet",
        "description": "Greet one person.",
        "parameters": {"name": {"type": "string"}},
        "returns": {"type": "string"},
    })


class GeneratorTests(unittest.TestCase):
    def test_exact_choice_masks_the_highest_illegal_score(self) -> None:
        model = make_model("fn_greet\n")
        answer = TokenGenerator(model=model).choose(
            "prompt",
            {"greet": "fn_greet", "add": "fn_add"},
        )
        self.assertEqual(answer, "greet")

    def test_negative_decimal_ends_at_comma(self) -> None:
        model = make_model("-12.5,")
        answer = TokenGenerator(model=model).number("prompt", False)
        self.assertEqual(answer, -12.5)

    def test_integer_has_no_decimal_token(self) -> None:
        model = make_model(" 12,")
        answer = TokenGenerator(model=model).number("prompt", True)
        self.assertEqual(answer, 12)

    def test_free_string_stops_at_quote_and_blocks_newline(self) -> None:
        model = make_model('Shrek"', invalid_id=10)
        answer = TokenGenerator(model=model).string('prompt ending in "')
        self.assertEqual(answer, "Shrek")


class CallerTests(unittest.TestCase):
    def test_greeting_uses_selection_then_string_completion(self) -> None:
        model = make_model("fn_greet\n", 'Shrek"', invalid_id=10)
        caller = FunctionCaller(
            functions=[greet_spec()],
            generator=TokenGenerator(model=model),
        )
        call = caller.call(Request(prompt="Greet Shrek"))
        self.assertIsNotNone(call)
        assert call is not None
        self.assertEqual(call.name, "fn_greet")
        self.assertEqual(call.parameters, {"name": "Shrek"})
        self.assertIn("Registered functions", caller._selection_prompt(
            "Greet Shrek"
        ))
        self.assertIn('fn_greet(name="', caller._completion_prompt(
            "Greet Shrek", "fn_greet", "name", {}, numeric=False
        ))

    def test_fn_none_is_omitted(self) -> None:
        model = make_model("fn_none\n")
        caller = FunctionCaller(
            functions=[greet_spec()],
            generator=TokenGenerator(model=model),
        )
        self.assertIsNone(caller.call(Request(prompt="Travel to Mars")))

    def test_two_numbers_use_two_model_completions(self) -> None:
        function = FunctionSpec.model_validate({
            "name": "fn_add",
            "description": "Add two numbers.",
            "parameters": {
                "a": {"type": "number"},
                "b": {"type": "number"},
            },
            "returns": {"type": "number"},
        })
        model = make_model("fn_add\n", " 2,", " 3.5,")
        caller = FunctionCaller(
            functions=[function],
            generator=TokenGenerator(model=model),
        )
        call = caller.call(Request(prompt="Add 2 and 3.5"))
        self.assertIsNotNone(call)
        assert call is not None
        self.assertEqual(call.parameters, {"a": 2.0, "b": 3.5})

    def test_boolean_and_allowed_value_stay_exact_choices(self) -> None:
        function = FunctionSpec.model_validate({
            "name": "fn_configure",
            "description": "Configure a feature.",
            "parameters": {
                "enabled": {"type": "boolean"},
                "mode": {
                    "type": "string",
                    "allowed_values": ["fast", "safe"],
                },
            },
            "returns": {"type": "string"},
        })
        model = make_model("fn_configure\n", "true\n", '"fast"\n')
        caller = FunctionCaller(
            functions=[function],
            generator=TokenGenerator(model=model),
        )
        call = caller.call(Request(prompt="Use fast mode"))
        self.assertIsNotNone(call)
        assert call is not None
        self.assertEqual(
            call.parameters, {"enabled": True, "mode": "fast"}
        )

    def test_bad_number_uses_a_typed_fallback(self) -> None:
        function = FunctionSpec.model_validate({
            "name": "fn_number",
            "description": "Use a number.",
            "parameters": {"a": {"type": "number"}},
            "returns": {"type": "number"},
        })
        model = make_model("fn_number\n", " ,")
        caller = FunctionCaller(
            functions=[function],
            generator=TokenGenerator(model=model),
        )
        call = caller.call(Request(prompt="Use a number"))
        self.assertIsNotNone(call)
        assert call is not None
        self.assertEqual(call.parameters, {"a": 0.0})


class FileTests(unittest.TestCase):
    def test_invalid_json_has_a_clear_error(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "broken.json"
            source.write_text("[{]", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "invalid JSON"):
                load_requests(source)

    def test_unknown_type_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "functions.json"
            source.write_text(json.dumps([{
                "name": "fn_bad",
                "description": "Bad schema.",
                "parameters": {"x": {"type": "mystery"}},
                "returns": {"type": "string"},
            }]), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "unsupported"):
                load_functions(source)

    def test_writer_emits_only_the_required_keys(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            target = Path(directory) / "nested" / "results.json"
            write_calls(target, [FunctionCall(
                prompt="Greet Alice",
                name="fn_greet",
                parameters={"name": "Alice"},
            )])
            payload = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(set(payload[0]), {
                "prompt", "name", "parameters"
            })

    def test_complete_read_process_write_path(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            functions = root / "functions.json"
            requests = root / "requests.json"
            output = root / "nested" / "results.json"
            functions.write_text(
                json.dumps([greet_spec().model_dump()]),
                encoding="utf-8",
            )
            requests.write_text(
                json.dumps([{"prompt": "Greet Shrek"}]),
                encoding="utf-8",
            )
            calls, warnings = run(
                Settings(
                    functions_path=functions,
                    input_path=requests,
                    output_path=output,
                ),
                make_model("fn_greet\n", 'Shrek"', invalid_id=10),
            )
            self.assertEqual(warnings, [])
            self.assertEqual(calls[0].parameters, {"name": "Shrek"})
            self.assertEqual(
                json.loads(output.read_text(encoding="utf-8"))[0]["name"],
                "fn_greet",
            )


if __name__ == "__main__":
    unittest.main()
