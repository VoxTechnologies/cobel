from harness.validate import schema_ok, SchemaResult

VALID = """
skill: relocate
objects:
  part: { ref: part, estimated_mass: 1.0 N }
body:
  sequence:
    - let: part_t
      from: { sense.locate: { target_ref: part, modality: auto } }
    - grasp.pinch: { target: part_t, force_budget: 6 N, tactile_target: auto, slip_response: retighten }
    - grasp.release: { grasp_handle: active }
"""

MALFORMED = "skill: x\nbody:\n  sequence:\n    - not_a_category.bogus: {}\n"


def test_valid_skill_passes_schema():
    r = schema_ok(VALID)
    assert isinstance(r, SchemaResult)
    assert r.ok, r.error


def test_malformed_skill_fails_schema():
    r = schema_ok(MALFORMED)
    assert not r.ok
    assert r.error
