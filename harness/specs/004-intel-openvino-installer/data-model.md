# Data Model: Intel OpenVINO Installer

## Installation Context

Represents the local information used to select a method.

| Field | Meaning | Validation |
|-------|---------|------------|
| `system` | Windows, Linux, macOS, or unsupported | Required for live planning |
| `architecture` | Normalized CPU architecture | Must be explicit or `unknown` |
| `context` | Native, WSL, container, Docker target, or Yocto target | Must not be inferred from a package manager alone |
| `ecosystem` | Python, Conda, Node.js, C++, system, Docker, Yocto | User request may override default |
| `version_request` | Explicit, maintenance, latest, or unspecified | Must retain requested value |
| `permissions` | Whether requested actions appear authorized | Unknown is not treated as allowed |
| `available_tools` | Detected package managers and runtimes | Values are detected facts only |

## Installation Method

Represents one documented route.

| Field | Meaning | Validation |
|-------|---------|------------|
| `id` | Stable method identifier | Must be one of the supported profiles |
| `platforms` | Systems and contexts where it applies | Selected context must match |
| `ecosystem` | Package/runtime ecosystem | Must match user intent |
| `packages` | Packages or artifacts to install | No hidden packages |
| `commands` | Ordered commands for plan/apply modes | Commands must be rendered from structured data |
| `prerequisites` | Required tools, permissions and drivers | Missing prerequisites block or downgrade the plan |
| `alternatives` | Documented fallback methods | Never silently executed |

## Installation Plan

The immutable preview shown before any mutation.

| Field | Meaning | Validation |
|-------|---------|------------|
| `status` | `ready`, `blocked`, `unsupported`, or `needs_confirmation` | `ready` still requires confirmation to apply |
| `method` | Selected `Installation Method` | Required when status is actionable |
| `version` | Resolved or requested version | Must include support-status note |
| `actions` | Ordered commands and file/environment changes | Must not include unapproved driver actions |
| `confirmation_required` | Whether apply needs explicit approval | Always true for mutations |
| `warnings` | Version, driver, conflict and compatibility limits | Must remain visible |

## Verification Result

Evidence collected after execution or a fixture simulation.

| Field | Meaning | Validation |
|-------|---------|------------|
| `status` | `passed`, `partial`, `failed`, or `not_run` | Never pass when a required check is unknown |
| `installed_version` | Detected runtime/package version | May be `unknown` |
| `runtime_import` | Import or executable check | Must be separate from device visibility |
| `devices` | Runtime-visible devices when applicable | Does not prove workload support |
| `components` | Optional component checks | Missing optional components are not core failures |
| `issues` | Sanitized failure details | Must not contain secrets or arbitrary output |
