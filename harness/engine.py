"""Reference-engine coverage: which Skill ISA primitives the rfl retarget engine
actually lowers (its `enum Primitive`), plus a walker that extracts the primitive ids
a skill uses. A skill using a primitive outside ENGINE_18 that fails retarget is an
engine coverage gap (`beyond_engine`), not a model error.

ENGINE_18 transcribed from rfl/crates/rfl-core/src/skill_isa.rs `enum Primitive`
(rfl commit recorded in harness/schema/SOURCE.md).
"""
from __future__ import annotations

import yaml

ENGINE_18: frozenset[str] = frozenset(
    {
        "sense.locate", "sense.inspect",
        "grasp.pinch", "grasp.release",
        "transport.move_to_pose", "transport.carry",
        "reach.align", "reach.retract", "reach.scan", "reach.hover",
        "force.insert_fit", "force.screw", "force.unscrew",
        "force.press_button", "force.wipe", "force.snap_engage", "force.cut",
        "in_hand.flip",
    }
)

# The seven Skill ISA categories (+ the `ext` namespace). A primitive id is
# `category.name`; any other dotted key (e.g. an offset field) is not a primitive.
_CATEGORIES = ("reach", "grasp", "in_hand", "transport", "place", "force", "sense", "ext")


def _looks_like_primitive(key: object) -> bool:
    return isinstance(key, str) and "." in key and key.split(".", 1)[0] in _CATEGORIES


def _walk(node: object, out: set[str]) -> None:
    if isinstance(node, dict):
        for k, v in node.items():
            if _looks_like_primitive(k):
                out.add(k)
            _walk(v, out)
    elif isinstance(node, list):
        for item in node:
            _walk(item, out)


def primitives_used(skill_yaml: str) -> set[str]:
    out: set[str] = set()
    _walk(yaml.safe_load(skill_yaml), out)
    return out
