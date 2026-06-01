# cobel

Demand-side existence proof for [RFL](https://github.com/robotfoundationlayer/rfl): demonstrate
that a real foundation model can emit valid, retargetable RFL **Skill ISA**.

`cobel` is the matched half of [Milchick](https://github.com/robotfoundationlayer/rfl/blob/main/docs/design/2026-05-31-pincherx-existence-proof-design.md)
(the supply-side proof, a real embodiment). Milchick holds the embodiment fixed and the planner
trivial; `cobel` holds the planner real (Claude) and the embodiment a set of descriptors. Together
they bracket the RFL roadmap's "(VLA, embodiment) pair" existence-proof milestone.

## What it proves

A frontier foundation model, given the Skill ISA spec + a task + a scene (but **not** the
embodiment), emits valid, schema-conformant, retargetable Skill ISA across novel tasks — at a
measured pass rate (`pass@1` / `pass@k`, spec-only vs few-shot). It does **not** claim that
action-token VLAs (π0 / OpenVLA / Octo) emit RFL — those operate below the Skill ISA; the ISA's
natural emitter is the planner / VLM tier.

## Layout

- `planner/` — the planner-adapter contract + a deterministic mock + a real Claude emitter
- `harness/` — schema + retarget validation; pass-rate reporting
- `tasks/` — task + scene inputs (novel; not the RFL examples)
- `run.py` — `--planner mock|claude --mode spec-only|few-shot`
- `results/` — generated pass-rate tables (the published artifact)

Authoritative design: `rfl/docs/design/2026-06-01-demand-side-existence-proof-design.md`.

Private during development. To be published Apache-2.0 when the proof runs.
