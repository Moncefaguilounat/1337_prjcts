"""Three short token loops: exact choice, number, and free string."""

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from .llm import LanguageModel


class TokenGenerator(BaseModel):
    """Use the model's highest-scoring legal next token at each step."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    model: LanguageModel
    max_tokens: int = Field(default=96, ge=1, le=512)
    visualize: bool = False

    @staticmethod
    def _pick(
        scores: list[float],
        legal: list[int] | None,
        blocked: int | None = None,
    ) -> int:
        """mask the illegal logits and return the bigger score token from the
        legal ones"""
        logits = np.asarray(scores, dtype=np.float64)
        if logits.ndim != 1 or logits.size == 0:
            raise ValueError("model returned an invalid logits vector")
        if legal is not None:
            usable = [token for token in legal if 0 <= token < logits.size]
            if not usable:
                raise ValueError("no legal token has a model score")
            masked = np.full(logits.shape, -np.inf)
            masked[usable] = logits[usable]
            logits = masked
        if blocked is not None and 0 <= blocked < logits.size:
            logits[blocked] = -np.inf
        logits[np.isnan(logits)] = -np.inf
        if np.all(np.isneginf(logits)):
            raise ValueError("model gave no usable next-token score")
        return int(np.argmax(logits))

    def _show(self, step: int, token: int) -> None:
        if self.visualize:
            print(f"step {step:02d}: {self.model.decode([token])!r}")

    def choose(self, prompt: str, options: dict[str, str]) -> str:
        """Generate exactly one encoded option followed by a newline."""
        targets = {
            label: self.model.encode(text + "\n")
            for label, text in options.items()
        }
        if not targets:
            raise ValueError("there are no choices to generate")
        prompt_ids = self.model.encode(prompt)
        generated: list[int] = []
        for step in range(1, min(30, self.max_tokens) + 1):
            for label, target in targets.items():
                if generated == target:
                    return label
            position = len(generated)
            legal = list({
                target[position]
                for target in targets.values()
                if target[:position] == generated and position < len(target)
            })
            if not legal:
                raise ValueError("no function or literal can continue")
            token = self._pick(
                self.model.logits(prompt_ids + generated), legal
            )
            generated.append(token)
            self._show(step, token)
        for label, target in targets.items():
            if generated == target:
                return label
        raise ValueError("exact-choice generation did not finish")

    def number(self, prompt: str, integer_only: bool) -> int | float:
        """Start with a sign, then permit digits and a finishing comma."""
        prompt_ids = self.model.encode(prompt)
        sign_tokens = [self.model.one_token(" "), self.model.one_token("-")]
        spaced_minus = self.model.encode(" -")
        if len(spaced_minus) == 1:
            sign_tokens.append(spaced_minus[0])
        generated = [
            self._pick(self.model.logits(prompt_ids), sign_tokens)
        ]
        self._show(1, generated[0])

        legal = [
            self.model.one_token(str(digit))
            for digit in range(10)
        ] + [self.model.one_token(",")]
        if not integer_only:
            legal.append(self.model.one_token("."))
        comma = self.model.one_token(",")

        for step in range(1, min(20, self.max_tokens) + 1):
            token = self._pick(
                self.model.logits(prompt_ids + generated), legal
            )
            generated.append(token)
            self._show(step + 1, token)
            if token == comma:
                break
        else:
            raise ValueError("number generation did not reach a comma")

        text = self.model.decode(generated).replace(",", "").strip()
        try:
            return int(text) if integer_only else float(text)
        except ValueError as error:
            raise ValueError(f"generated value {text!r} is not a number") \
                from error

    def string(self, prompt: str) -> str:
        """Generate freely, blocking newline, until a quote appears."""
        prompt_ids = self.model.encode(prompt)
        newline = self.model.one_token("\n")
        generated: list[int] = []
        for step in range(1, min(50, self.max_tokens) + 1):
            logits = self.model.logits(prompt_ids + generated)
            token = self._pick(logits, None, newline)
            generated.append(token)
            self._show(step, token)
            if '"' in self.model.decode([token]):
                return self.model.decode(generated).split('"', 1)[0]
        raise ValueError("string generation did not reach a quote")
