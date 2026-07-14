from __future__ import annotations

from pydantic import BaseModel, Field


class RawServiceAccount(BaseModel):
    namespace: str
    name: str
    annotations: dict[str, str] = Field(default_factory=dict)


class RawWorkload(BaseModel):
    kind: str
    namespace: str
    name: str
    service_account: str = "default"


class RawAssociation(BaseModel):
    namespace: str
    service_account: str
    role_arn: str


class RawPolicyStatement(BaseModel):
    effect: str
    action: list[str]
    resource: list[str]
    principal: dict[str, list[str]] = Field(default_factory=dict)


class RawPolicyDocument(BaseModel):
    statements: list[RawPolicyStatement]


class RawPolicy(BaseModel):
    name: str
    document: RawPolicyDocument


class RawRole(BaseModel):
    arn: str
    name: str
    trust_policy: RawPolicyDocument
    attached_policies: list[RawPolicy] = Field(default_factory=list)
    inline_policies: list[RawPolicy] = Field(default_factory=list)


class RawClusterFixture(BaseModel):
    cluster: str
    service_accounts: list[RawServiceAccount]
    workloads: list[RawWorkload]
    pod_identity_associations: list[RawAssociation] = Field(default_factory=list)


class RawIamFixture(BaseModel):
    roles: list[RawRole]


class FixtureBundle(BaseModel):
    cluster: RawClusterFixture
    iam: RawIamFixture


class Finding(BaseModel):
    id: str
    kind: str
    severity: str
    summary: str
    evidence: list[str]


class ServiceAccountIdentity(BaseModel):
    namespace: str
    name: str
    role_arns: list[str]
    workload_count: int


class WorkloadIdentity(BaseModel):
    kind: str
    namespace: str
    name: str
    service_account: str
    effective_role_arns: list[str]
    node_role_fallback_risk: bool


class RoleSummary(BaseModel):
    arn: str
    name: str
    account_id: str
    wildcard_permissions: bool
    cross_account_trust: bool


class IdentitySnapshot(BaseModel):
    cluster: str
    service_accounts: list[ServiceAccountIdentity]
    workloads: list[WorkloadIdentity]
    roles: list[RoleSummary]
    findings: list[Finding]


class ExplainedRole(BaseModel):
    arn: str
    cross_account_trust: bool
    wildcard_permissions: bool


class WorkloadExplanation(BaseModel):
    workload: str
    service_account: str
    effective_role_arns: list[str]
    node_role_fallback_risk: bool
    trust_note: str
    evidence: list[str]
    roles: list[ExplainedRole]


class WorkloadDelta(BaseModel):
    workload: str
    before_role_arns: list[str]
    after_role_arns: list[str]
    before_node_role_fallback_risk: bool
    after_node_role_fallback_risk: bool


class SnapshotDiff(BaseModel):
    before_cluster: str
    after_cluster: str
    added_findings: list[Finding]
    removed_findings: list[Finding]
    changed_workloads: list[WorkloadDelta]
