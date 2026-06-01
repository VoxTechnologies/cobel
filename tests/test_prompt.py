from pathlib import Path

P = Path(__file__).parents[1] / "planner" / "prompts" / "skill-isa-system.md"


def test_prompt_covers_the_essentials():
    text = P.read_text()
    for token in ["sequence", "let", "grasp.pinch", "force_budget", "Output", "YAML"]:
        assert token in text, token


def test_spec_only_prompt_is_blind():
    # The spec-only system prompt must NOT embed a worked example skill from the rfl
    # examples — that would make the "blind" claim false (few-shot mode adds one separately).
    assert "cable-insertion" not in P.read_text()
