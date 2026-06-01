from pathlib import Path

from harness.validate import retarget_outcome, Outcome

DESC = Path(__file__).parents[1] / "harness" / "descriptors" / "allegro.yaml"
ALLEGRO = DESC.read_text()

# 18-set skill allegro declares (grasp.pinch, transport, sense.locate): retarget_ok.
LOWERABLE = """
skill: relocate
objects: { part: { ref: part, estimated_mass: 1.0 N } }
body:
  sequence:
    - let: part_t
      from: { sense.locate: { target_ref: part, modality: auto } }
    - grasp.pinch: { target: part_t, force_budget: 6 N, tactile_target: auto, slip_response: retighten }
    - transport.move_to_pose: { target_pose: { frame: world, offset: { along: +z, distance: 40 mm } } }
    - grasp.release: { grasp_handle: active }
    - reach.retract: { direction: -tool_axis, distance: 50 mm }
"""

# Valid full-spec skill using place.put_down (NOT in ENGINE_18): beyond_engine.
BEYOND = """
skill: drop
objects: { part: { ref: part, estimated_mass: 1.0 N }, tray: { ref: tray } }
body:
  sequence:
    - let: part_t
      from: { sense.locate: { target_ref: part, modality: auto } }
    - grasp.pinch: { target: part_t, force_budget: 6 N, tactile_target: auto, slip_response: retighten }
    - place.put_down: { target_surface: { frame: tray }, approach: -z }
"""


def test_lowerable_skill_retargets_ok():
    out = retarget_outcome(LOWERABLE, ALLEGRO)
    assert out.kind == "retarget_ok", f"{out.kind}: {out.detail}"


def test_beyond_engine_primitive_classified():
    out = retarget_outcome(BEYOND, ALLEGRO)
    assert out.kind == "beyond_engine", f"{out.kind}: {out.detail}"
