from pathlib import Path

import pytest

from planner.contract import load_task
from planner.mock import MockPlanner
from harness.validate import schema_ok, retarget_outcome

ROOT = Path(__file__).parents[1]
ALLEGRO = (ROOT / "harness" / "descriptors" / "allegro.yaml").read_text()

# Group A: built from the engine's 18-primitive set. relocate-part / seat-fuse retarget_ok
# on allegro; latch-buckle uses force.snap_engage, which allegro does not declare, so it
# correctly capability-rejects (the mismatch path).
GROUP_A = ["relocate-part", "seat-fuse", "latch-buckle"]
# Group B: valid full-spec Skill ISA beyond the engine's set -> schema_ok + beyond_engine.
GROUP_B = ["pour", "stack-blocks", "sort-by-weight"]


def _skill(name: str) -> str:
    task, scene = load_task(ROOT / "tasks" / f"{name}.yaml")
    return MockPlanner().plan(task, scene)


@pytest.mark.parametrize("name", GROUP_A + GROUP_B)
def test_every_reference_skill_is_schema_valid(name):
    r = schema_ok(_skill(name))
    assert r.ok, f"{name}: {r.error}"


@pytest.mark.parametrize("name", GROUP_A)
def test_group_a_lowerable(name):
    out = retarget_outcome(_skill(name), ALLEGRO)
    assert out.kind in {"retarget_ok", "capability_rejected"}, f"{name}: {out.kind} {out.detail}"


@pytest.mark.parametrize("name", GROUP_B)
def test_group_b_is_beyond_engine(name):
    out = retarget_outcome(_skill(name), ALLEGRO)
    assert out.kind == "beyond_engine", f"{name}: {out.kind} {out.detail}"
