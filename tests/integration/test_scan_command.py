import json
from pathlib import Path

from typer.testing import CliRunner

from podsleuth.cli import app


def test_scan_matches_expected_fixture_output() -> None:
    fixture_dir = Path("tests/fixtures/identity-snapshot")
    expected = json.loads((fixture_dir / "expected-scan.json").read_text())

    result = CliRunner().invoke(app, ["scan", "--fixtures", str(fixture_dir)])

    assert result.exit_code == 0
    assert json.loads(result.stdout) == expected


def test_scan_reports_missing_fixture_directory_file() -> None:
    fixture_dir = Path("tests/fixtures/missing-iam")
    result = CliRunner().invoke(app, ["scan", "--fixtures", str(fixture_dir)])

    assert result.exit_code == 2
