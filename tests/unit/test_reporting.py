from pathlib import Path

from podsleuth.analysis import build_snapshot
from podsleuth.fixtures import load_fixture_snapshot
from podsleuth.reporting import build_workload_explanation, render_workload_explanation


def test_build_workload_explanation_describes_bound_role() -> None:
    bundle = load_fixture_snapshot(Path("tests/fixtures/identity-snapshot"))
    explanation = build_workload_explanation(bundle, build_snapshot(bundle), "payments/api")

    assert explanation.node_role_fallback_risk is False
    assert explanation.roles[0].wildcard_permissions is True
    assert explanation.roles[0].explicit_deny is True


def test_render_workload_explanation_mentions_evidence() -> None:
    bundle = load_fixture_snapshot(Path("tests/fixtures/identity-snapshot"))
    explanation = build_workload_explanation(bundle, build_snapshot(bundle), "ops/metrics")
    rendered = render_workload_explanation(explanation)

    assert "Node-role fallback risk: yes" in rendered
    assert "Evidence: workload:ops/metrics, service-account:ops/default" in rendered


def test_render_workload_explanation_mentions_trust_mode_and_explicit_deny() -> None:
    bundle = load_fixture_snapshot(Path("tests/fixtures/identity-snapshot"))
    explanation = build_workload_explanation(bundle, build_snapshot(bundle), "payments/api")
    rendered = render_workload_explanation(explanation)

    assert "trust mode: federated" in rendered
    assert "explicit deny present" in rendered
