from pathlib import Path

from typer.testing import CliRunner

from podsleuth.cli import app


def test_explain_renders_expected_workload_summary() -> None:
    fixture_dir = Path("tests/fixtures/identity-snapshot")

    result = CliRunner().invoke(app, ["explain", "payments/api", "--fixtures", str(fixture_dir)])

    assert result.exit_code == 0
    assert "Workload: payments/api" in result.stdout
    assert "Service account: payments/api" in result.stdout
    assert "wildcard permissions" in result.stdout
    assert "Missing role evidence: arn:aws:iam::111122223333:role/payments-shadow" in result.stdout


def test_explain_returns_distinct_exit_code_for_missing_workload() -> None:
    fixture_dir = Path("tests/fixtures/identity-snapshot")

    result = CliRunner().invoke(
        app, ["explain", "payments/missing", "--fixtures", str(fixture_dir)]
    )

    assert result.exit_code == 3
