"""Validation gates for an emitted Skill ISA YAML string.

PRIMARY: schema conformance against the full 50-primitive skill-isa.schema.json — the
spec-grounded definition of "valid Skill ISA" (does not depend on engine coverage).
SECONDARY: retarget through the published rfl binding (added in Task 5), a stronger but
coverage-bounded check.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import rfl  # the published PyO3 binding (rfl.retarget / rfl.RetargetError)
import yaml
from jsonschema import Draft202012Validator

from harness.engine import ENGINE_18, primitives_used

_SCHEMA_PATH = Path(__file__).parent / "schema" / "skill-isa.schema.json"


@lru_cache(maxsize=1)
def _validator() -> Draft202012Validator:
    return Draft202012Validator(json.loads(_SCHEMA_PATH.read_text()))


@dataclass(frozen=True)
class SchemaResult:
    ok: bool
    error: str = ""


def schema_ok(skill_yaml: str) -> SchemaResult:
    try:
        doc = yaml.safe_load(skill_yaml)
    except yaml.YAMLError as exc:
        return SchemaResult(False, f"yaml parse error: {exc}")
    if not isinstance(doc, dict):
        return SchemaResult(False, "top-level document is not a mapping")
    errs = sorted(_validator().iter_errors(doc), key=lambda e: list(e.path))
    if errs:
        return SchemaResult(False, errs[0].message)
    return SchemaResult(True)


@dataclass(frozen=True)
class Outcome:
    kind: str  # "retarget_ok" | "capability_rejected" | "beyond_engine" | "malformed"
    detail: str = ""


def retarget_outcome(skill_yaml: str, descriptor_yaml: str) -> Outcome:
    try:
        jsonl = rfl.retarget(skill_yaml, descriptor_yaml)
        return Outcome("retarget_ok", f"{len(jsonl.splitlines())} action(s)")
    except rfl.RetargetError as exc:
        msg = str(exc)
        if "capability_absent" in msg:
            return Outcome("capability_rejected", msg)
        # Separate engine coverage gaps from genuine emission errors: a primitive
        # outside the engine's implemented set fails because the engine is incomplete,
        # not because the model erred.
        if primitives_used(skill_yaml) - ENGINE_18:
            return Outcome("beyond_engine", msg)
        return Outcome("malformed", msg)
