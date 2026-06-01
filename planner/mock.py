"""Deterministic reference planner: returns a hand-authored reference skill per task,
keyed by a stable substring of the instruction. Offline, no network — the CI gate and
the "reference planner" half of the proof.
"""
from __future__ import annotations

from pathlib import Path

from planner.contract import Scene, TaskSpec

_REF_DIR = Path(__file__).parents[1] / "reference_skills"

# Map an instruction substring to its reference-skill file. Substring keying lets the
# task wording vary without breaking the lookup.
_ROUTES: list[tuple[str, str]] = [
    ("staging tray", "relocate-part.yaml"),
]


class MockPlanner:
    def plan(self, task: TaskSpec, scene: Scene) -> str:
        for needle, fname in _ROUTES:
            if needle in task.instruction:
                return (_REF_DIR / fname).read_text()
        raise KeyError(f"MockPlanner has no reference skill for: {task.instruction!r}")
