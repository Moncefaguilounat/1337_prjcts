*This project has been created as part of the 42 curriculum by <login>.*

# call_me_maybe

## What it does

The program turns each natural-language request into a function name and
arguments. It never calls the function or calculates its return value.
Successful calls are written as an array of objects with exactly the keys
`prompt`, `name`, and `parameters`.

## Run

```bash
uv sync
uv run python -m src
```

Optional paths:

```bash
uv run python -m src \
  --functions_definition data/input/functions_definition.json \
  --input data/input/function_calling_tests.json \
  --output data/output/function_calling_results.json
```

`--visualize` prints selected tokens. `--max-tokens` sets a global cap;
the normal function, number, and string loops use at most 30, 20, and 50
tokens respectively. `make test` and `make lint` run the checks.

## Execution path

```text
python -m src
  -> __main__.py reads command-line options
  -> data.py reads and validates the function/request JSON
  -> llm.py loads Qwen through the public llm_sdk API
  -> caller.py processes one request at a time
       -> decoder.py selects one exact function name
       -> decoder.py completes each declared argument
       -> caller.py checks the argument schema
  -> data.py writes the result JSON
```

There is no vocabulary loader and no JSON-string state machine. The model
wrapper uses only the SDK's public `encode`, `decode`, and
`get_logits_from_input_ids` methods.

## Generation algorithm

Function selection presents the dynamically loaded function descriptions
and an internal `fn_none` option. Each name plus a newline is encoded.
At each step, only token IDs that continue one of those exact sequences
retain their logits; the highest remaining score is chosen. A complete
sequence selects that function. `fn_none` causes the request to be omitted.

For each argument, the program presents a code-completion prompt containing
the original request, selected function, and already extracted arguments:

```text
-> Greet Shrek
fn_greet(name="
```

String extraction generates greedily, masks the newline token, and stops
at a token whose decoded text contains a quote. Number extraction first
chooses a space or minus sign, then masks everything except encoded digits,
a finishing comma, and a decimal point for non-integer types. The comma
ends generation; the decoded text is converted to `int` or `float`.

Booleans, nulls, enums, and explicit allowed values are generated as exact
encoded choices. They are needed because the evaluation also checks
allowed values and declared argument types. A failed extraction receives
a type-compatible fallback and a warning. Final Pydantic validation and
`json.dump` ensure the output file is parseable JSON with the exact keys.

## Design decisions and limits

This is a deliberately small, independently written implementation of the
simple reference-style prompt and token loops. `caller.py` decides which
LLM question comes next; `decoder.py` contains only the three short loops;
`llm.py` converts SDK tensors to ordinary Python lists; `data.py` owns
validated input and output. Every project class uses Pydantic.

The function-choice and finite-value paths are hard-constrained. Free
string extraction and digits/comma number extraction are simpler but weaker
than a complete JSON grammar: a token containing a newline could slip
through the single-newline mask, an escaped quote can stop a string early,
and a poorly formed decimal can trigger fallback. JSON serialization
guarantees parseability, not semantic accuracy. The real Qwen model and
private Moulinette still must be run to measure the subject's >90% accuracy
and <5-minute targets.

## Tests and resources

The deterministic tests cover exact-choice masking, number and string
generation, multiple arguments, booleans, allowed values, typed fallback,
file errors, exact output keys, and one complete read/process/write path.

Resources: the supplied subject, correction scale, `llm_sdk`, Python
`json`/`argparse` documentation, Pydantic validation, and NumPy masking.
AI assistance was used for an independently written implementation and
tests. The student must inspect, understand, and defend the final code.
