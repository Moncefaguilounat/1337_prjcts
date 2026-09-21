"""Deterministic SDK replacement used by the tests."""

from pydantic import BaseModel


class ScriptedModel(BaseModel):
    """Emit queued answers while always preferring an illegal token."""

    answers: list[list[int]]
    invalid_id: int = 255
    answer_index: int = 0
    token_index: int = 0

    @classmethod
    def from_texts(
        cls,
        *answers: str,
        invalid_id: int = 255,
    ) -> "ScriptedModel":
        """Create the fake backend from queued text answers."""
        encoded_answers = [
            [ord(character) for character in answer]
            for answer in answers
        ]
        return cls(answers=encoded_answers, invalid_id=invalid_id)

    def encode(self, text: str) -> list[list[int]]:
        """Represent every ASCII character by its code point."""
        return [[ord(character) for character in text]]

    def decode(self, token_ids: list[int]) -> str:
        """Decode test token IDs back into characters."""
        return "".join(chr(token_id) for token_id in token_ids)

    def get_logits_from_input_ids(
        self,
        input_ids: list[int],
    ) -> list[float]:
        """Prefer an illegal ID globally and the queued answer second."""
        del input_ids
        if self.answer_index >= len(self.answers):
            raise AssertionError("the fake model has no queued answer")
        answer = self.answers[self.answer_index]
        wanted = answer[self.token_index]
        logits = [-100.0] * 256
        logits[self.invalid_id] = 100.0
        logits[wanted] = 10.0
        self.token_index += 1
        if self.token_index == len(answer):
            self.answer_index += 1
            self.token_index = 0
        return logits
