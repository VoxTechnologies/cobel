from pathlib import Path

from planner.contract import load_task
from planner.mock import MockPlanner
from harness.validate import schema_ok, retarget_outcome

ROOT = Path(__file__).parents[1]
ALLEGRO = (ROOT / "harness" / "descriptors" / "allegro.yaml").read_text()


def test_mock_relocate_part_schema_and_retarget():
    task, scene = load_task(ROOT / "tasks" / "relocate-part.yaml")
    skill = MockPlanner().plan(task, scene)
    r = schema_ok(skill)
    assert r.ok, r.error
    out = retarget_outcome(skill, ALLEGRO)
    assert out.kind == "retarget_ok", f"{out.kind}: {out.detail}"
