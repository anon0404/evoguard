from __future__ import annotations

import os
import time
import random

from guardrail_gym.models.base import BaseModelAdapter, ModelResponse


class OpenAIModelAdapter(BaseModelAdapter):
    def __init__(self, model_name: str = "gpt-4.1"):
        self.model_name = model_name

    def generate(self, prompt: str, system_prompt: str | None = None) -> ModelResponse:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY not set")

        try:
            from openai import OpenAI
        except Exception as e:
            raise RuntimeError("openai package not installed") from e

        client = OpenAI(api_key=api_key)

        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        start = time.time()
        last_error = None
        resp = None
        for attempt in range(3):
            try:
                resp = client.chat.completions.create(
                    model=self.model_name,
                    messages=messages,
                )
                break
            except Exception as e:
                last_error = e
                time.sleep((2 ** attempt) + random.random())
        if resp is None:
            raise last_error
        elapsed = (time.time() - start) * 1000.0

        text = ""
        if getattr(resp, "choices", None):
            text = resp.choices[0].message.content or ""

        raw = resp.model_dump() if hasattr(resp, "model_dump") else {"repr": str(resp)}

        return ModelResponse(
            text=text,
            raw=raw,
            latency_ms=elapsed,
            cost_usd=0.0,
            model_name=self.model_name,
        )
