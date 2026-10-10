"""
AIntern — Groq LLM Client
Single factory for creating LangChain-compatible Groq chat models.
"""

import re

from langchain_groq import ChatGroq
from app.config import settings


def get_llm(temperature: float = 0.7) -> ChatGroq:
    """
    Return a configured ChatGroq instance.

    Args:
        temperature: Creativity level (0 = deterministic, 1 = creative).
                     Use lower values (0.2–0.4) for structured JSON output.
                     Use higher values (0.6–0.9) for varied simulation content.

    Note:
        Reasoning models (e.g. Qwen) may emit <think>...</think> blocks.
        These are stripped downstream by strip_think_tags() before JSON parsing.
    """
    return ChatGroq(
        api_key=settings.groq_api_key,
        model=settings.groq_model,
        temperature=temperature,
    )


def strip_think_tags(text: str) -> str:
    """
    Fallback cleaner: remove any <think>...</think> blocks from model output.
    Handles cases where reasoning_format is not supported by the model.
    """
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
