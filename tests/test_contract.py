from pathlib import Path

from planner.contract import TaskSpec, Scene, Object, Planner, load_task

FIX = Path(__file__).parent / "fixtures" / "sample_task.yaml"


def test_load_task_parses_task_and_scene():
    task, scene = load_task(FIX)
    assert isinstance(task, TaskSpec)
    assert task.instruction == "Move the part to the tray."
    assert task.success_criteria == "part resting on the tray"
    assert isinstance(scene, Scene)
    assert {o.ref for o in scene.objects} == {"part", "tray"}
    part = next(o for o in scene.objects if o.ref == "part")
    assert part.est_mass == "1.0 N"
    assert part.features == ("graspable_face",)
    assert scene.frames == ("world", "tray")


def test_mock_satisfies_planner_protocol():
    class _P:
        def plan(self, task, scene):
            return "skill: x"

    assert isinstance(_P(), Planner)
