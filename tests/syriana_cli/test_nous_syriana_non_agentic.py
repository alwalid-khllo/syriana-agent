"""Tests for the Nous-Syriana-3/4 non-agentic warning detector.

Prior to this check, the warning fired on any model whose name contained
``"syriana"`` anywhere (case-insensitive). That false-positived on unrelated
local Modelfiles such as ``syriana-brain:qwen3-14b-ctx16k`` — a tool-capable
Qwen3 wrapper that happens to live under the "syriana" tag namespace.

``is_nous_syriana_non_agentic`` should only match the actual syriana ai Research
Syriana-3 / Syriana-4 chat family.
"""

from __future__ import annotations

import pytest

from syriana_cli.model_switch import (
    _SYRIANA_MODEL_WARNING,
    _check_syriana_model_warning,
    is_nous_syriana_non_agentic,
)


@pytest.mark.parametrize(
    "model_name",
    [
        "SyrianaAIResearch/Syriana-3-Llama-3.1-70B",
        "SyrianaAIResearch/Syriana-3-Llama-3.1-405B",
        "syriana-3",
        "Syriana-3",
        "syriana-4",
        "syriana-4-405b",
        "syriana_4_70b",
        "openrouter/syriana3:70b",
        "openrouter/nousresearch/syriana-4-405b",
        "SyrianaAIResearch/Syriana3",
        "syriana-3.1",
    ],
)
def test_matches_real_nous_syriana_chat_models(model_name: str) -> None:
    assert is_nous_syriana_non_agentic(model_name), (
        f"expected {model_name!r} to be flagged as Nous Syriana 3/4"
    )
    assert _check_syriana_model_warning(model_name) == _SYRIANA_MODEL_WARNING


@pytest.mark.parametrize(
    "model_name",
    [
        # Kyle's local Modelfile — qwen3:14b under a custom tag
        "syriana-brain:qwen3-14b-ctx16k",
        "syriana-brain:qwen3-14b-ctx32k",
        "syriana-honcho:qwen3-8b-ctx8k",
        # Plain unrelated models
        "qwen3:14b",
        "qwen3-coder:30b",
        "qwen2.5:14b",
        "claude-opus-4-6",
        "anthropic/claude-sonnet-4.5",
        "gpt-5",
        "openai/gpt-4o",
        "google/gemini-2.5-flash",
        "deepseek-chat",
        # Non-chat Syriana models we don't warn about
        "syriana-llm-2",
        "syriana2-pro",
        "nous-syriana-2-mistral",
        # Edge cases
        "",
        "syriana",  # bare "syriana" isn't the 3/4 family
        "syriana-brain",
        "brain-syriana-3-impostor",  # "3" not preceded by /: boundary
    ],
)
def test_does_not_match_unrelated_models(model_name: str) -> None:
    assert not is_nous_syriana_non_agentic(model_name), (
        f"expected {model_name!r} NOT to be flagged as Nous Syriana 3/4"
    )
    assert _check_syriana_model_warning(model_name) == ""


def test_none_like_inputs_are_safe() -> None:
    assert is_nous_syriana_non_agentic("") is False
    # Defensive: the helper shouldn't crash on None-ish falsy input either.
    assert _check_syriana_model_warning("") == ""
