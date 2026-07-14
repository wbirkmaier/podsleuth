from pathlib import Path

from podsleuth.analysis import build_snapshot
from podsleuth.fixtures import load_fixture_snapshot


def test_build_snapshot_flags_expected_findings() -> None:
    snapshot = build_snapshot(load_fixture_snapshot(Path("tests/fixtures/identity-snapshot")))

    assert [finding.kind for finding in snapshot.findings] == [
        "cross_account_trust",
        "explicit_deny",
        "node_role_fallback_risk",
        "orphaned_pod_identity_association",
        "shared_service_account",
        "wildcard_permission",
    ]


def test_build_snapshot_preserves_effective_role_bindings() -> None:
    snapshot = build_snapshot(load_fixture_snapshot(Path("tests/fixtures/identity-snapshot")))
    workloads = {(item.namespace, item.name): item for item in snapshot.workloads}

    assert workloads[("payments", "api")].effective_role_arns == [
        "arn:aws:iam::111122223333:role/payments-api-irsa"
    ]
    assert workloads[("ops", "metrics")].node_role_fallback_risk is True


def test_build_snapshot_records_trust_mode_and_explicit_deny() -> None:
    snapshot = build_snapshot(load_fixture_snapshot(Path("tests/fixtures/identity-snapshot")))
    roles = {item.name: item for item in snapshot.roles}

    assert roles["payments-api-irsa"].trust_mode == "federated"
    assert roles["payments-api-irsa"].explicit_deny is True
