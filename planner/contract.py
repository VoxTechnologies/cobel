"""The planner-adapter contract: the demand-side analogue of RFL's ReferenceDriver.

A Planner turns a natural-language task + a structured scene into Skill ISA YAML text,
embodiment-agnostically (Principle 1): the scene describes the world, never the robot.
The embodiment descriptor enters only later, at the harness's retarget step.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol, runtime_checkable

import yaml


@dataclass(frozen=True)
class Object:
    ref: str
    kind: str
    est_mass: str | None = None
    geometry: str | None = None
    pose_hint: str | None = None
    features: tuple[str, ...] = ()


@dataclass(frozen=True)
class Scene:
    objects: tuple[Object, ...]
    frames: tuple[str, ...]
    notes: str | None = None


@dataclass(frozen=True)
class TaskSpec:
    instruction: str
    success_criteria: str | None = None


@runtime_checkable
class Planner(Protocol):
    def plan(self, task: TaskSpec, scene: Scene) -> str:
        """Emit Skill ISA YAML text for the task in the given scene."""
        ...


def load_task(path: str | Path) -> tuple[TaskSpec, Scene]:
    data = yaml.safe_load(Path(path).read_text())
    t, s = data["task"], data["scene"]
    objects = tuple(
        Object(
            ref=o["ref"],
            kind=o["kind"],
            est_mass=o.get("est_mass"),
            geometry=o.get("geometry"),
            pose_hint=o.get("pose_hint"),
            features=tuple(o.get("features", [])),
        )
        for o in s["objects"]
    )
    scene = Scene(objects=objects, frames=tuple(s["frames"]), notes=s.get("notes"))
    return (
        TaskSpec(instruction=t["instruction"], success_criteria=t.get("success_criteria")),
        scene,
    )
