from __future__ import annotations

from collections import defaultdict

from podsleuth.models import (
    Finding,
    FixtureBundle,
    IdentitySnapshot,
    RawPolicyDocument,
    RoleSummary,
    ServiceAccountIdentity,
    WorkloadIdentity,
)


def _account_id_from_arn(arn: str) -> str:
    parts = arn.split(":")
    return parts[4] if len(parts) > 4 else "unknown"


def _has_wildcard_permissions(policy_documents: list[RawPolicyDocument]) -> bool:
    for policy_document in policy_documents:
        for statement in policy_document.statements:
            if statement.effect != "Allow":
                continue
            if any(action == "*" or action.endswith(":*") for action in statement.action):
                return True
            if any(resource == "*" for resource in statement.resource):
                return True
    return False


def _has_cross_account_trust(role_arn: str, policy_documents: list[RawPolicyDocument]) -> bool:
    role_account_id = _account_id_from_arn(role_arn)
    for policy_document in policy_documents:
        for statement in policy_document.statements:
            for principals in statement.principal.values():
                for principal in principals:
                    if (
                        principal.startswith("arn:aws:iam::")
                        and _account_id_from_arn(principal) != role_account_id
                    ):
                        return True
    return False


def build_snapshot(bundle: FixtureBundle) -> IdentitySnapshot:
    association_map: dict[tuple[str, str], list[str]] = defaultdict(list)
    findings: list[Finding] = []

    for association in bundle.cluster.pod_identity_associations:
        association_map[(association.namespace, association.service_account)].append(
            association.role_arn
        )

    service_account_map = {
        (service_account.namespace, service_account.name): service_account
        for service_account in bundle.cluster.service_accounts
    }
    workload_counts: dict[tuple[str, str], int] = defaultdict(int)

    workloads: list[WorkloadIdentity] = []
    for workload in sorted(
        bundle.cluster.workloads, key=lambda item: (item.namespace, item.name, item.kind)
    ):
        workload_counts[(workload.namespace, workload.service_account)] += 1
        service_account = service_account_map.get((workload.namespace, workload.service_account))
        role_arns: list[str] = []
        if service_account is not None:
            irsa_role = service_account.annotations.get("eks.amazonaws.com/role-arn")
            if irsa_role is not None:
                role_arns.append(irsa_role)
        role_arns.extend(association_map.get((workload.namespace, workload.service_account), []))
        deduplicated_role_arns = sorted(set(role_arns))
        workloads.append(
            WorkloadIdentity(
                kind=workload.kind,
                namespace=workload.namespace,
                name=workload.name,
                service_account=workload.service_account,
                effective_role_arns=deduplicated_role_arns,
                node_role_fallback_risk=not deduplicated_role_arns,
            )
        )
        if not deduplicated_role_arns:
            findings.append(
                Finding(
                    id=f"node-fallback:{workload.namespace}/{workload.name}",
                    kind="node_role_fallback_risk",
                    severity="medium",
                    summary=(
                        f"{workload.kind} {workload.namespace}/{workload.name} "
                        "has no workload identity binding"
                    ),
                    evidence=[f"workload:{workload.namespace}/{workload.name}"],
                )
            )

    service_accounts: list[ServiceAccountIdentity] = []
    for service_account in sorted(
        bundle.cluster.service_accounts,
        key=lambda item: (item.namespace, item.name),
    ):
        bound_role_arns: list[str] = []
        irsa_role = service_account.annotations.get("eks.amazonaws.com/role-arn")
        if irsa_role is not None:
            bound_role_arns.append(irsa_role)
        bound_role_arns.extend(
            association_map.get((service_account.namespace, service_account.name), [])
        )
        identity = ServiceAccountIdentity(
            namespace=service_account.namespace,
            name=service_account.name,
            role_arns=sorted(set(bound_role_arns)),
            workload_count=workload_counts[(service_account.namespace, service_account.name)],
        )
        service_accounts.append(identity)
        if identity.workload_count > 1:
            findings.append(
                Finding(
                    id=f"shared-service-account:{identity.namespace}/{identity.name}",
                    kind="shared_service_account",
                    severity="medium",
                    summary=(
                        f"Service account {identity.namespace}/{identity.name} is shared by "
                        f"{identity.workload_count} workloads"
                    ),
                    evidence=[f"service-account:{identity.namespace}/{identity.name}"],
                )
            )

    for association in sorted(
        bundle.cluster.pod_identity_associations,
        key=lambda item: (item.namespace, item.service_account, item.role_arn),
    ):
        key = (association.namespace, association.service_account)
        if key not in service_account_map:
            findings.append(
                Finding(
                    id=f"orphaned-association:{association.namespace}/{association.service_account}",
                    kind="orphaned_pod_identity_association",
                    severity="high",
                    summary=(
                        "Pod identity association references a service account "
                        "that is not present in the snapshot"
                    ),
                    evidence=[f"association:{association.namespace}/{association.service_account}"],
                )
            )

    roles: list[RoleSummary] = []
    for role in sorted(bundle.iam.roles, key=lambda item: item.arn):
        policy_documents = [role.trust_policy]
        policy_documents.extend(policy.document for policy in role.attached_policies)
        policy_documents.extend(policy.document for policy in role.inline_policies)
        role_summary = RoleSummary(
            arn=role.arn,
            name=role.name,
            account_id=_account_id_from_arn(role.arn),
            wildcard_permissions=_has_wildcard_permissions(
                [policy.document for policy in role.attached_policies]
                + [policy.document for policy in role.inline_policies]
            ),
            cross_account_trust=_has_cross_account_trust(role.arn, [role.trust_policy]),
        )
        roles.append(role_summary)
        if role_summary.wildcard_permissions:
            findings.append(
                Finding(
                    id=f"wildcard:{role.name}",
                    kind="wildcard_permission",
                    severity="high",
                    summary=f"Role {role.name} allows wildcard action or resource access",
                    evidence=[f"role:{role.arn}"],
                )
            )
        if role_summary.cross_account_trust:
            findings.append(
                Finding(
                    id=f"cross-account:{role.name}",
                    kind="cross_account_trust",
                    severity="medium",
                    summary=f"Role {role.name} trusts a principal in another AWS account",
                    evidence=[f"role:{role.arn}"],
                )
            )

    return IdentitySnapshot(
        cluster=bundle.cluster.cluster,
        service_accounts=service_accounts,
        workloads=workloads,
        roles=roles,
        findings=sorted(findings, key=lambda item: item.id),
    )
