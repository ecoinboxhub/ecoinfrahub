from __future__ import annotations
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.backend.assistants import SYSTEM_PROMPTS, get_expert_response


def test_system_prompts_exist():
    assert "engineering" in SYSTEM_PROMPTS
    assert "climate" in SYSTEM_PROMPTS
    assert "proposal" in SYSTEM_PROMPTS
    assert "research" in SYSTEM_PROMPTS


def test_system_prompts_not_empty():
    for key, prompt in SYSTEM_PROMPTS.items():
        assert len(prompt) > 50, f"Prompt for {key} is too short"
        assert "EcoInfraMind" in prompt, f"Prompt for {key} missing app name"


def test_system_prompts_no_markdown():
    for key, prompt in SYSTEM_PROMPTS.items():
        assert "#" not in prompt, f"Prompt for {key} contains markdown headers"
        assert "**" not in prompt, f"Prompt for {key} contains bold markdown"
        assert "emoji" in prompt.lower() or "Do not use" in prompt, f"Prompt for {key} missing emoji instruction"


def test_expert_response_generator():
    gen = get_expert_response("test query", "engineering", stream=True)
    assert gen is not None


def test_expert_response_default_type():
    gen = get_expert_response("test query", "unknown_type", stream=True)
    assert gen is not None


def test_run():
    test_system_prompts_exist()
    test_system_prompts_not_empty()
    test_system_prompts_no_markdown()
    test_expert_response_generator()
    test_expert_response_default_type()
    print("All assistant tests passed!")


if __name__ == "__main__":
    test_run()
