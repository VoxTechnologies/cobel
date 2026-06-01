"""cobel proof runner.

  python run.py --planner mock                       # offline, deterministic (CI gate)
  python run.py --planner claude --mode spec-only    # needs ANTHROPIC_API_KEY
  python run.py --planner claude --mode few-shot --samples 5

Emits two tables (schema-validity headline + retarget-outcome map) and writes them to
results/<planner>-<mode>.md.
"""
from __future__ import annotations

import argparse
from pathlib import Path

from planner.contract import load_task
from planner.mock import MockPlanner
from harness.validate import schema_ok, retarget_outcome
from harness.report import Row, render_tables

ROOT = Path(__file__).parent
TASKS = sorted(p.stem for p in (ROOT / "tasks").glob("*.yaml"))
DESCRIPTORS = {p.stem: p.read_text() for p in sorted((ROOT / "harness" / "descriptors").glob("*.yaml"))}


def _planner(name: str, mode: str):
    if name == "mock":
        return MockPlanner()
    from planner.claude import ClaudePlanner  # lazy: needs anthropic + an API key

    return ClaudePlanner(mode=mode)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--planner", choices=["mock", "claude"], default="mock")
    ap.add_argument("--mode", choices=["spec-only", "few-shot"], default="spec-only")
    ap.add_argument("--samples", type=int, default=1)
    args = ap.parse_args()

    planner = _planner(args.planner, args.mode)
    rows: list[Row] = []
    for task_name in TASKS:
        task, scene = load_task(ROOT / "tasks" / f"{task_name}.yaml")
        passes, best_skill, first_error = 0, None, ""
        for _ in range(args.samples):
            skill = planner.plan(task, scene)
            r = schema_ok(skill)
            if r.ok:
                passes += 1
                best_skill = best_skill or skill
            elif not first_error:
                first_error = r.error
        retarget: dict[str, str] = {}
        if best_skill is not None:
            for dname, dyaml in DESCRIPTORS.items():
                retarget[dname] = retarget_outcome(best_skill, dyaml).kind
        rows.append(
            Row(task=task_name, mode=args.mode, schema_ok=passes > 0,
                retarget=retarget, n=args.samples, schema_pass=passes,
                schema_error=first_error)
        )

    md = f"# cobel results — planner={args.planner} mode={args.mode} samples={args.samples}\n\n"
    md += render_tables(rows)
    out = ROOT / "results" / f"{args.planner}-{args.mode}.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text(md)
    print(md)
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
