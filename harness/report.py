"""Aggregate per-(task, mode, sample) results into the two published tables:
(a) the headline schema_ok pass@1 / pass@k; (b) the retarget-outcome breakdown per
descriptor (which doubles as an honest reference-engine coverage map).
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Row:
    task: str
    mode: str
    schema_ok: bool                       # did the best sample pass the schema gate
    retarget: dict[str, str] = field(default_factory=dict)  # descriptor -> outcome kind
    n: int = 1                            # samples drawn
    schema_pass: int = 1                  # samples that passed schema (for pass@k)


def render_tables(rows: list[Row]) -> str:
    out: list[str] = [
        "## (a) Headline — schema validity (the demand-side claim)\n",
        "| task | mode | schema_ok | pass@1 | pass@k |",
        "|---|---|---|---|---|",
    ]
    for r in rows:
        p1 = "1" if r.schema_pass >= 1 else "0"
        pk = f"{r.schema_pass}/{r.n}"
        out.append(f"| {r.task} | {r.mode} | {'ok' if r.schema_ok else 'FAIL'} | {p1} | {pk} |")

    descriptors = sorted({d for r in rows for d in r.retarget})
    out += [
        "\n## (b) Retarget outcomes (engine-coverage map)\n",
        "| task | mode | " + " | ".join(descriptors) + " |",
        "|---|---|" + "---|" * len(descriptors),
    ]
    for r in rows:
        cells = " | ".join(r.retarget.get(d, "-") for d in descriptors)
        out.append(f"| {r.task} | {r.mode} | {cells} |")
    return "\n".join(out) + "\n"
