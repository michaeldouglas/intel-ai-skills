# Runtime Skill Report Contract

Every new runtime skill MUST return the common report keys defined in
`../data-model.md` in JSON mode. Text mode is a human-readable rendering of the
same information and MUST NOT expose additional unredacted command output.

Required keys:

`schema_version`, `collection_status`, `context`, `request`, `selection`,
`plan`, `execution`, `verification`, `warnings`, `issues`.

## Status vocabulary

- `complete`: all requested facts were collected.
- `partial`: useful facts exist but one or more optional checks were unavailable.
- `blocked`: the requested action could not safely begin because a prerequisite
  or confirmation is missing.
- `failed`: an attempted action failed.
- `not_run`: an action was intentionally not executed.

## Safety contract

- Plan mode MUST be read-only.
- Apply mode MUST require explicit confirmation for mutation.
- Verify mode MUST not imply model quality, accuracy, or performance from an
  import or device list alone.
- Commands and outputs MUST be bounded and redacted.
