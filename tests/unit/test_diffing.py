from pathlib import Path

from podsleuth.diffing import diff_snapshots
from podsleuth.snapshot_io import load_snapshot


def test_diff_snapshots_reports_added_removed_findings_and_workload_changes() -> None:
    before = load_snapshot(Path("tests/fixtures/diff/before.json"))
    after = load_snapshot(Path("tests/fixtures/diff/after.json"))

    snapshot_diff = diff_snapshots(before, after)

    assert [finding.id for finding in snapshot_diff.added_findings] == [
        "shared-service-account:payments/api"
    ]
    assert [finding.id for finding in snapshot_diff.removed_findings] == [
        "node-fallback:ops/metrics"
    ]
    assert snapshot_diff.changed_workloads[0].workload == "ops/metrics"
    assert snapshot_diff.changed_workloads[0].after_role_arns == [
        "arn:aws:iam::111122223333:role/ops-observability"
    ]
