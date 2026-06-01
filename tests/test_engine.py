from harness.engine import ENGINE_18, primitives_used


def test_engine_18_has_exactly_18():
    assert len(ENGINE_18) == 18
    assert "grasp.pinch" in ENGINE_18 and "place.put_down" not in ENGINE_18


def test_primitives_used_walks_body():
    skill = """
skill: t
body:
  sequence:
    - let: x
      from: { sense.locate: { target_ref: a } }
    - grasp.pinch: { target: x }
    - place.put_down: { target_surface: { frame: tray } }
"""
    assert primitives_used(skill) == {"sense.locate", "grasp.pinch", "place.put_down"}


def test_primitives_used_ignores_algebra_keys():
    skill = "skill: t\nbody:\n  sequence:\n    - reach.retract: { distance: 10 mm }\n"
    assert primitives_used(skill) == {"reach.retract"}
