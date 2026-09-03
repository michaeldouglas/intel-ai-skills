# Contributing

## Branch flow

This repository uses a controlled promotion flow:

```text
feature/<kebab-case-name> -> develop -> main
```

Rules:

1. Create every change from `develop` in a branch named
   `feature/<kebab-case-name>`.
2. Open the feature pull request with base `develop`.
3. Wait for the required checks and review, then merge the feature pull
   request into `develop`.
4. Promote the integrated `develop` branch to `main` with a pull request whose
   head is exactly `develop`.
5. Never commit or push directly to `main`. Do not merge a feature branch
   directly into `main`.

Example:

```powershell
git fetch origin
git switch develop
git pull --ff-only origin develop
git switch -c feature/add-openvino-probe
# implement the change
git push --set-upstream origin feature/add-openvino-probe
```

The GitHub Actions branch-policy check validates the allowed pull-request
directions. GitHub branch protection must additionally require pull requests,
the branch-policy check, project quality checks, and disable administrator
and bypass exceptions on both `develop` and `main`.

## Spec Kit and Graphify

Feature work follows the Spec Kit artifacts under `harness/specs/`: write or
update the specification, plan, tasks, analysis, implementation, evaluation,
and quality review in that order as applicable. For codebase questions, use
Graphify's scoped query/path/explain commands when its index is available, and
run `graphify update .` after modifying code or product artifacts.

## Pull requests

Pull requests must state the source and target branches, link the relevant
Spec Kit feature directory, describe test/evaluation results, and call out
any constitution or release-gate exception. Promotion PRs from `develop` to
`main` should summarize the integrated changes and confirm that `develop` is
green.
