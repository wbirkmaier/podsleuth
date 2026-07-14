from __future__ import annotations

from podsleuth.exceptions import PodSleuthError
from podsleuth.models import IdentitySnapshot


def _node_id(prefix: str, value: str) -> str:
    cleaned = value.replace("/", "_").replace(":", "_").replace("-", "_")
    return f"{prefix}_{cleaned}"


def render_mermaid(snapshot: IdentitySnapshot) -> str:
    lines = ["graph TD"]

    for workload in snapshot.workloads:
        workload_ref = f"{workload.namespace}/{workload.name}"
        service_account_ref = f"{workload.namespace}/{workload.service_account}"
        workload_id = _node_id("workload", workload_ref)
        service_account_id = _node_id("sa", service_account_ref)
        lines.append(f'    {workload_id}["{workload.kind} {workload_ref}"]')
        lines.append(f'    {service_account_id}["ServiceAccount {service_account_ref}"]')
        lines.append(f"    {workload_id} --> {service_account_id}")
        if workload.effective_role_arns:
            for role_arn in workload.effective_role_arns:
                role_id = _node_id("role", role_arn)
                lines.append(f'    {role_id}["Role {role_arn}"]')
                lines.append(f"    {service_account_id} --> {role_id}")
        elif workload.node_role_fallback_risk:
            fallback_id = _node_id("risk", f"node-fallback:{workload_ref}")
            lines.append(f'    {fallback_id}{{"Node role fallback risk"}}')
            lines.append(f"    {workload_id} -.-> {fallback_id}")

    for finding in snapshot.findings:
        finding_id = _node_id("finding", finding.id)
        lines.append(f'    {finding_id}{{"{finding.kind}"}}')
        for evidence in finding.evidence:
            if evidence.startswith("workload:"):
                workload_id = _node_id("workload", evidence.removeprefix("workload:"))
                lines.append(f"    {workload_id} -.-> {finding_id}")
            elif evidence.startswith("service-account:"):
                service_account_id = _node_id("sa", evidence.removeprefix("service-account:"))
                lines.append(f"    {service_account_id} -.-> {finding_id}")
            elif evidence.startswith("role:"):
                role_id = _node_id("role", evidence.removeprefix("role:"))
                lines.append(f"    {role_id} -.-> {finding_id}")

    return "\n".join(lines)


def render_snapshot(snapshot: IdentitySnapshot, output_format: str) -> str:
    if output_format != "mermaid":
        raise PodSleuthError(f"unsupported render format: {output_format}")
    return render_mermaid(snapshot)
