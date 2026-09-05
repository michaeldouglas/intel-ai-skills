# Installation Plan Contract

The bundled helper accepts a JSON fixture for deterministic tests and emits a
stable JSON report for the agent. Live collection and command execution use the
same shape.

## Top-level report

```json
{
  "schema_version": "1.0",
  "collection_status": "complete",
  "context": {},
  "selection": {},
  "plan": {},
  "verification": {},
  "issues": []
}
```

## Safety rules

- Planning MUST use `collection_status` and MUST NOT execute package-manager
  commands.
- A plan that mutates the environment MUST set
  `plan.confirmation_required` to `true`.
- Apply mode MUST be invoked only after the agent receives explicit user
  confirmation.
- Command output MUST be sanitized before it is placed in `issues`.
- Driver, BIOS, benchmark and arbitrary-file operations are not part of the
  v1 command contract.

## Selection fields

```json
{
  "method": "pip",
  "ecosystem": "python",
  "version": "maintenance",
  "reason": "Python project with virtual-environment support",
  "alternatives": ["conda", "archive"]
}
```

## Verification fields

```json
{
  "status": "partial",
  "installed_version": "2026.3.0",
  "runtime_import": "passed",
  "devices": [],
  "components": {},
  "issues": [
    {
      "kind": "driver",
      "status": "not_checked",
      "message": "GPU driver readiness is outside installer scope"
    }
  ]
}
```
