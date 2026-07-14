# Examples

```bash
uv run podsleuth scan --fixtures tests/fixtures/identity-snapshot
uv run podsleuth explain payments/api --fixtures tests/fixtures/identity-snapshot
uv run podsleuth diff tests/fixtures/diff/before.json tests/fixtures/diff/after.json
uv run podsleuth render tests/fixtures/diff/after.json --format mermaid
```

Current findings in the shipped fixture include:

- shared service account usage across two workloads
- wildcard IAM permissions
- cross-account trust
- explicit deny statements in a bound role policy
- orphaned pod identity association
- a workload falling back to the node role path because no workload identity is attached
