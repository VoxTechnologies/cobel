"""The PincherX-100 (a real 4-DOF, no-F/T, ~$600 arm) in the retarget map shows RFL spanning
embodiments from a dexterous hand down to the low end without leaking:

- relocate-part (pinch + transport + locate) retargets cleanly onto PincherX too;
- the force tasks (seat-fuse / latch-buckle) correctly capability_reject on a no-F/T arm;
- the place.*/sense.weigh/branch tasks are beyond the reference engine either way.
"""
from pathlib import Path

import pytest

from planner.contract import load_task
from planner.mock import MockPlanner
from harness.validate import retarget_outcome

ROOT = Path(__file__).parents[1]
PINCHERX = (ROOT / "harness" / "descriptors" / "pincherx-100.yaml").read_text()

EXPECTED = {
    "relocate-part": "retarget_ok",        # same agnostic skill lowers onto a low-end arm
    "seat-fuse": "capability_rejected",    # no F/T -> force.insert_fit rejected
    "latch-buckle": "capability_rejected",  # no F/T -> force.snap_engage rejected
    "pour": "beyond_engine",
    "stack-blocks": "beyond_engine",
    "sort-by-weight": "beyond_engine",
}


@pytest.mark.parametrize("name,expected", EXPECTED.items())
def test_pincherx_outcomes(name, expected):
    task, scene = load_task(ROOT / "tasks" / f"{name}.yaml")
    out = retarget_outcome(MockPlanner().plan(task, scene), PINCHERX)
    assert out.kind == expected, f"{name}: {out.kind} ({out.detail})"
