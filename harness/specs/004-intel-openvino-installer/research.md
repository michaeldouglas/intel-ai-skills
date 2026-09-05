# Research: Intel OpenVINO Installer

**Scope**: OpenVINO 2026 documentation bundled under `harness/docs/2026/`.
**Accessed**: 2026-09-05.

## Decision: Keep one standalone installer with method profiles

**Rationale**: The documentation exposes several installation mechanisms, but
the user needs one entry point that chooses a compatible method. The skill will
route by operating system, architecture, target ecosystem, execution context,
and requested component without requiring another skill.

**Alternatives considered**:

- One skill per package manager: rejected because users would need to know the
  correct method before asking for installation.
- Documentation-only advisor: rejected because the requested skill must execute
  the selected installation after confirmation.

## Decision: Prefer isolated Python installation for the default Python flow

The PyPI guide creates a virtual environment, upgrades Pip, and installs the
`openvino` package. This is the least invasive path for Python users.

Source: `docs/2026/get-started/install-openvino/install-openvino-pip.html`.

## Decision: Route native system installation by platform

- Windows: prefer versioned WinGet when available; archive installation is a
  documented fallback.
- Ubuntu/Debian-like Linux: APT is the native package path; archive and Pip are
  alternatives.
- RHEL-like Linux: YUM is the native package path.
- openSUSE: Zypper is the native package path.
- macOS: Homebrew or the macOS archive are supported paths.

Sources:

- `install-openvino-winget.html`
- `install-openvino-archive-windows.html`
- `install-openvino-apt.html`
- `install-openvino-yum.html`
- `install-openvino-zypper.html`
- `install-openvino-brew.html`
- `install-openvino-archive-macos.html`
- `install-openvino-archive-linux.html`

## Decision: Preserve ecosystem-specific package managers

Conda, npm, vcpkg, Conan, Docker and Yocto are separate profiles. The skill
must not silently replace an existing project ecosystem with Pip or a global
system package.

Sources:

- `install-openvino-conda.html`
- `install-openvino-npm.html`
- `install-openvino-vcpkg.html`
- `install-openvino-conan.html`
- `install-openvino-docker-linux.html`
- `install-openvino-yocto.html`

## Decision: Treat GenAI as an optional component profile

OpenVINO GenAI has separate PyPI, npm and archive instructions. It is installed
only when requested, and its verification is separate from core OpenVINO.

Source: `install-openvino-genai.html`.

## Decision: Version selection is explicit and evidence-aware

The OpenVINO 2026.3 landing page states that 2026.3 is not an LTS release and
lists 2026.3.1 as development and 2025.4.1 as maintenance. The installer will
prefer a maintenance version for production-oriented requests, but will honor
an explicitly requested version and warn about its support status.

Source: `docs/2026/get-started/install-openvino.html`.

## Decision: Do not install drivers automatically in v1

The configuration pages describe additional GPU and NPU drivers, OpenCL,
Level Zero, kernel and WSL requirements. These are system-specific and can have
larger side effects than installing the runtime. The installer will report
missing prerequisites and link to the appropriate official guidance, while
leaving driver changes to an explicit future workflow.

Sources:

- `docs/2026/get-started/install-openvino/configurations.html`
- `configurations/configurations-intel-gpu.html`
- `configurations/configurations-intel-npu.html`

## Decision: Validate installation separately from workload compatibility

The post-install check will verify package/runtime visibility, version and
available devices when the selected ecosystem supports it. It will not claim
that a particular model, precision or performance target is supported.

## Decision: Do not use the discontinued `openvino-dev` metapackage

The troubleshooting guide says to use `openvino` and optional extras such as
`openvino[tensorflow2]` or `openvino[onnx]`. The skill will reflect that rule.

Source: `configurations/troubleshooting-install-config.html`.
