"""Only the public encode, decode, and logits calls of the supplied SDK."""

from importlib import import_module
from typing import Any

from pydantic import BaseModel, ConfigDict


class LanguageModel(BaseModel):
    """Give the rest of the program simple Python lists instead of tensors."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    backend: Any

    @classmethod
    def load(cls, name: str) -> "LanguageModel":
        sdk = import_module("llm_sdk")
        constructor = getattr(sdk, "Small_LLM_Model", None)
        if not callable(constructor):
            raise ValueError("llm_sdk does not provide Small_LLM_Model")
        return cls(backend=constructor(name))

    # @classmethod
    # def from_backend(cls, backend: Any) -> "LanguageModel":
    #     """Inject a deterministic model during tests without loading Qwen."""
    #     return cls(backend=backend)
    #
    def encode(self, text: str) -> list[int]:
        value = self.backend.encode(text)
        if hasattr(value, "squeeze"):
            value = value.squeeze()
        if hasattr(value, "tolist"):
            value = value.tolist()
        while isinstance(value, list) and len(value) == 1 \
                and isinstance(value[0], list):
            value = value[0]
        if isinstance(value, int):
            return [value]
        if not isinstance(value, list):
            raise ValueError("llm_sdk returned invalid token IDs")
        return [int(token_id) for token_id in value]

    def one_token(self, text: str) -> int:
        """Find one token ID using encode; no vocabulary file is needed."""
        ids = self.encode(text)
        if len(ids) != 1:
            raise ValueError(f"{text!r} does not encode to one token")
        return ids[0]

    def decode(self, ids: list[int]) -> str:
        decoder = getattr(self.backend, "decode", None)
        if not callable(decoder):
            raise ValueError("llm_sdk does not provide decode")
        return str(decoder(ids))

    def logits(self, ids: list[int]) -> list[float]:
        value = self.backend.get_logits_from_input_ids(ids)
        if hasattr(value, "tolist"):
            value = value.tolist()
        while isinstance(value, list) and len(value) == 1 \
                and isinstance(value[0], list):
            value = value[0]
        if not isinstance(value, list):
            raise ValueError("llm_sdk returned invalid logits")
        try:
            return [float(score) for score in value]
        except (TypeError, ValueError) as error:
            raise ValueError("llm_sdk returned non-numeric logits") from error
