from __future__ import annotations

from podsleuth.models import IdentitySnapshot, SnapshotDiff, WorkloadDelta


def diff_snapshots(before: IdentitySnapshot, after: IdentitySnapshot) -> SnapshotDiff:
    before_findings = {finding.id: finding for finding in before.findings}
    after_findings = {finding.id: finding for finding in after.findings}

    before_workloads = {f"{item.namespace}/{item.name}": item for item in before.workloads}
    after_workloads = {f"{item.namespace}/{item.name}": item for item in after.workloads}

    changed_workloads: list[WorkloadDelta] = []
    for workload_name in sorted(set(before_workloads) | set(after_workloads)):
        before_workload = before_workloads.get(workload_name)
        after_workload = after_workloads.get(workload_name)
        before_role_arns = (
            before_workload.effective_role_arns if before_workload is not None else []
        )
        after_role_arns = after_workload.effective_role_arns if after_workload is not None else []
        before_fallback = (
            before_workload.node_role_fallback_risk if before_workload is not None else False
        )
        after_fallback = (
            after_workload.node_role_fallback_risk if after_workload is not None else False
        )

        if before_role_arns != after_role_arns or before_fallback != after_fallback:
            changed_workloads.append(
                WorkloadDelta(
                    workload=workload_name,
                    before_role_arns=before_role_arns,
                    after_role_arns=after_role_arns,
                    before_node_role_fallback_risk=before_fallback,
                    after_node_role_fallback_risk=after_fallback,
                )
            )

    return SnapshotDiff(
        before_cluster=before.cluster,
        after_cluster=after.cluster,
        added_findings=[
            after_findings[key] for key in sorted(set(after_findings) - set(before_findings))
        ],
        removed_findings=[
            before_findings[key] for key in sorted(set(before_findings) - set(after_findings))
        ],
        changed_workloads=changed_workloads,
    )
