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

import yaml
from jsonschema import Draft202012Validator

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
