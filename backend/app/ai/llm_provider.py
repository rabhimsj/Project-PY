from __future__ import annotations

import hashlib
import json
from abc import ABC, abstractmethod
from typing import Any

from openai import OpenAI

from app.config import settings


class BaseProvider(ABC):
    @abstractmethod
    def generate_text(self, prompt: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def embed_text(self, text: str) -> list[float]:
        raise NotImplementedError


class LocalProvider(BaseProvider):
    def generate_text(self, prompt: str) -> str:
        lowered = prompt.lower()
        if "summary" in lowered:
            return "This summary is generated using a local offline reasoning model. Focus on the key ideas, definitions, and exam-relevant concepts first."
        if "career" in lowered:
            return "Based on the provided profile, prioritize foundational skills, hands-on projects, and interview-ready communication practice."
        if "plan" in lowered:
            return "Follow a balanced daily schedule: revise concepts, solve questions, and revisit weak topics in the final 30 minutes."
        return "Here is a practical academic answer based on the available context and study materials."

    def embed_text(self, text: str) -> list[float]:
        digest = hashlib.sha256(text.encode("utf-8")).digest()
        numbers = []
        for index in range(8):
            chunk = digest[index * 4 : (index + 1) * 4]
            value = int.from_bytes(chunk, byteorder="big") / float(2**32)
            numbers.append(round(value, 6))
        return numbers


class OpenAIProvider(BaseProvider):
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate_text(self, prompt: str) -> str:
        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )
        return response.output_text.strip()

    def embed_text(self, text: str) -> list[float]:
        response = self.client.embeddings.create(model="text-embedding-3-small", input=text)
        return response.data[0].embedding


def get_provider() -> BaseProvider:
    if settings.openai_api_key:
        return OpenAIProvider(settings.openai_api_key, settings.openai_model)
    return LocalProvider()
