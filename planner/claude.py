"""Real foundation-model emitter. Builds a cached system prompt from the distilled Skill
ISA spec and asks Claude to emit a Skill ISA YAML for a task + scene.

SDK verified in-session via the claude-api skill (2026-06-01):
  - model id: `claude-opus-4-8` (exact string, no date suffix).
  - Messages API: client.messages.create(model, max_tokens, system=[blocks], messages=[...]).
  - system as a list of text blocks lets us attach cache_control to the (large, stable)
    spec prompt: {"type": "text", "text": ..., "cache_control": {"type": "ephemeral"}}.
  - adaptive thinking: thinking={"type": "adaptive"} (Opus 4.8 — the only on-mode); its
    thinking block may precede the answer, so extract text-type blocks only.
  - Opus 4.8 removes temperature/top_p/top_k (they 400) — pass@k variance is inherent, not
    a temperature knob.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

from planner.contract import Scene, TaskSpec

_PROMPT = (Path(__file__).parent / "prompts" / "skill-isa-system.md").read_text()
_MODEL = "claude-opus-4-8"
_FENCE = re.compile(r"```(?:ya?ml)?\s*(.*?)\s*```", re.DOTALL)

# Few-shot anchor: a worked example skill from the co-located rfl repo (read only in
# few-shot mode). cobel and rfl are sibling repos under .../GitHub/.
_FEWSHOT_ANCHOR = (
    Path(__file__).parents[2] / "rfl" / "examples" / "01-cable-insertion" / "skill.yaml"
)


def extract_yaml(text: str) -> str:
    """Pull the YAML body out of a model response: a fenced block if present, else the
    whole text."""
    m = _FENCE.search(text)
    return (m.group(1) if m else text).strip()


def _text_of(resp) -> str:
    """Concatenate the text-type content blocks (skipping any thinking block)."""
    parts = []
    for b in resp.content:
        if getattr(b, "type", None) in (None, "text"):
            t = getattr(b, "text", "")
            if t:
                parts.append(t)
    return "".join(parts)


def _scene_block(scene: Scene) -> str:
    return yaml.safe_dump(
        {
            "objects": [
                {
                    "ref": o.ref,
                    "kind": o.kind,
                    **({"est_mass": o.est_mass} if o.est_mass else {}),
                    **({"features": list(o.features)} if o.features else {}),
                }
                for o in scene.objects
            ],
            "frames": list(scene.frames),
            **({"notes": scene.notes} if scene.notes else {}),
        },
        sort_keys=False,
    )


class ClaudePlanner:
    def __init__(self, mode: str = "spec-only", client=None, model: str = _MODEL):
        assert mode in {"spec-only", "few-shot"}
        self.mode = mode
        self.model = model
        if client is None:
            from anthropic import Anthropic

            client = Anthropic()  # reads ANTHROPIC_API_KEY
        self.client = client

    def _system(self) -> list[dict]:
        # Cache the large, stable spec prompt across every task (prefix-stable).
        blocks = [
            {"type": "text", "text": _PROMPT, "cache_control": {"type": "ephemeral"}}
        ]
        if self.mode == "few-shot":
            anchor = _FEWSHOT_ANCHOR.read_text()
            blocks.append(
                {"type": "text", "text": f"Format anchor (a different task):\n{anchor}"}
            )
        return blocks

    def plan(self, task: TaskSpec, scene: Scene) -> str:
        user = (
            f"Task: {task.instruction}\n"
            f"Success: {task.success_criteria or '(unspecified)'}\n\n"
            f"Scene:\n{_scene_block(scene)}\n\n"
            "Emit the Skill ISA YAML now."
        )
        resp = self.client.messages.create(
            model=self.model,
            max_tokens=8000,
            thinking={"type": "adaptive"},
            system=self._system(),
            messages=[{"role": "user", "content": user}],
        )
        return extract_yaml(_text_of(resp))
