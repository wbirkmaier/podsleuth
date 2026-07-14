import json
from pathlib import Path

from typer.testing import CliRunner

from podsleuth.cli import app


def test_diff_matches_expected_output() -> None:
    fixture_dir = Path("tests/fixtures/diff")
    expected = json.loads((fixture_dir / "expected-diff.json").read_text())

    result = CliRunner().invoke(
        app,
        ["diff", str(fixture_dir / "before.json"), str(fixture_dir / "after.json")],
    )

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected
