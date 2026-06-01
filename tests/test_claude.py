from pathlib import Path

from planner.contract import load_task
from planner.claude import ClaudePlanner, extract_yaml

ROOT = Path(__file__).parents[1]


def test_extract_yaml_strips_fences():
    assert extract_yaml("```yaml\nskill: x\n```").strip() == "skill: x"
    assert extract_yaml("```\nskill: y\n```").strip() == "skill: y"
    assert extract_yaml("skill: z\n").strip() == "skill: z"


class _Block:
    def __init__(self, text, type="text"):
        self.text = text
        self.type = type


class _Msg:
    def __init__(self, text):
        # A thinking block (empty text, skipped) then the answer text block.
        self.content = [_Block("", type="thinking"), _Block(text)]


class _FakeClient:
    def __init__(self):
        self.messages = self
        self.captured = {}

    def create(self, **kw):
        self.captured.update(kw)
        return _Msg("```yaml\nskill: relocate-part\nbody: { sequence: [] }\n```")


def test_plan_builds_messages_and_returns_yaml():
    task, scene = load_task(ROOT / "tasks" / "relocate-part.yaml")
    client = _FakeClient()
    p = ClaudePlanner(mode="spec-only", client=client)
    out = p.plan(task, scene)
    assert out.startswith("skill:"), out
    assert client.captured["model"]  # a model id was set
    blob = str(client.captured["messages"])
    assert "staging tray" in blob or "tray" in blob  # the task/scene reached the user message
    # spec-only must not inject the few-shot example-skill anchor (it may include the JSON
    # schema, whose prose references the example name — that is the contract, not an example).
    assert "Format anchor" not in str(client.captured["system"])


def test_few_shot_adds_the_example_anchor():
    task, scene = load_task(ROOT / "tasks" / "relocate-part.yaml")
    client = _FakeClient()
    ClaudePlanner(mode="few-shot", client=client).plan(task, scene)
    assert "Format anchor" in str(client.captured["system"])
