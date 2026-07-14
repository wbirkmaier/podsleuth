from pathlib import Path

from podsleuth.rendering import render_mermaid
from podsleuth.snapshot_io import load_snapshot


def test_render_mermaid_matches_expected_graph() -> None:
    snapshot = load_snapshot(Path("tests/fixtures/diff/after.json"))

    rendered = render_mermaid(snapshot)

    assert rendered == Path("tests/fixtures/diff/expected-graph.mmd").read_text().rstrip("\n")
