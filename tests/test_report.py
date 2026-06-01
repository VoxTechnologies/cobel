from harness.report import Row, render_tables


def test_render_tables_has_both_sections():
    rows = [
        Row(task="relocate-part", mode="spec-only", schema_ok=True,
            retarget={"allegro": "retarget_ok", "leap": "retarget_ok"}, n=3, schema_pass=3),
        Row(task="pour", mode="spec-only", schema_ok=True,
            retarget={"allegro": "beyond_engine"}, n=3, schema_pass=2),
    ]
    md = render_tables(rows)
    assert "schema_ok" in md and "retarget" in md.lower()
    assert "relocate-part" in md and "pour" in md
    assert "pass@k" in md
