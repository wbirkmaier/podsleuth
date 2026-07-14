from pathlib import Path

from typer.testing import CliRunner

from podsleuth.cli import app


def test_render_emits_expected_mermaid_graph() -> None:
    fixture_dir = Path("tests/fixtures/diff")
    expected = (fixture_dir / "expected-graph.mmd").read_text().rstrip("\n")

    result = CliRunner().invoke(
        app,
        ["render", str(fixture_dir / "after.json"), "--format", "mermaid"],
    )

    assert result.exit_code == 0
    assert result.stdout == expected + "\n"
