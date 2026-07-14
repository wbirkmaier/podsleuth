from __future__ import annotations

from podsleuth.exceptions import PodSleuthError
from podsleuth.models import ExplainedRole, FixtureBundle, IdentitySnapshot, WorkloadExplanation


def build_workload_explanation(
    bundle: FixtureBundle,
    snapshot: IdentitySnapshot,
    workload_ref: str,
) -> WorkloadExplanation:
    namespace, separator, name = workload_ref.partition("/")
    if separator == "" or not namespace or not name:
        raise PodSleuthError("workload must be provided as <namespace>/<name>")

    workload = next(
        (item for item in snapshot.workloads if item.namespace == namespace and item.name == name),
        None,
    )
    if workload is None:
        raise PodSleuthError(f"workload not found in snapshot: {workload_ref}", exit_code=3)

    role_map = {role.arn: role for role in snapshot.roles}
    explained_roles = [
        ExplainedRole(
            arn=role_arn,
            cross_account_trust=role_map[role_arn].cross_account_trust,
            wildcard_permissions=role_map[role_arn].wildcard_permissions,
        )
        for role_arn in workload.effective_role_arns
        if role_arn in role_map
    ]

    trust_note = (
        "No workload identity is bound, so access may fall back to the node role path."
        if workload.node_role_fallback_risk
        else (
            "Bound roles were found, but PodSleuth does not treat trust and policy evidence "
            "as proof of usable access."
        )
    )

    del bundle
    return WorkloadExplanation(
        workload=f"{workload.namespace}/{workload.name}",
        service_account=f"{workload.namespace}/{workload.service_account}",
        effective_role_arns=workload.effective_role_arns,
        node_role_fallback_risk=workload.node_role_fallback_risk,
        trust_note=trust_note,
        evidence=[
            f"workload:{workload.namespace}/{workload.name}",
            f"service-account:{workload.namespace}/{workload.service_account}",
        ],
        roles=explained_roles,
    )


def render_workload_explanation(explanation: WorkloadExplanation) -> str:
    lines = [
        f"Workload: {explanation.workload}",
        f"Service account: {explanation.service_account}",
        f"Node-role fallback risk: {'yes' if explanation.node_role_fallback_risk else 'no'}",
        explanation.trust_note,
    ]
    if explanation.roles:
        lines.append("Roles:")
        for role in explanation.roles:
            flags: list[str] = []
            if role.cross_account_trust:
                flags.append("cross-account trust")
            if role.wildcard_permissions:
                flags.append("wildcard permissions")
            flag_text = f" ({', '.join(flags)})" if flags else ""
            lines.append(f"- {role.arn}{flag_text}")
    else:
        lines.append("Roles: none")
    lines.append(f"Evidence: {', '.join(explanation.evidence)}")
    return "\n".join(lines)
