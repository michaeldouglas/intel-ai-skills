# Quickstart: Intel OpenVINO Installer

## Prerequisites

- Python available for the harness tests.
- The repository checkout contains `harness/candidates/intel-openvino-installer/`.
- No network access or physical accelerator is required for fixture scenarios.

## Plan-only scenario

```powershell
python skills/intel-openvino-installer/scripts/openvino_installer.py --format json --mode plan
```

Expected result: a platform-aware plan is emitted and no package-manager,
download, driver or environment mutation occurs.

## Fixture scenario

```powershell
python skills/intel-openvino-installer/scripts/openvino_installer.py `
  --fixture harness/fixtures/openvino-installer/environments/windows-python.json `
  --format json --mode plan
```

Expected result: the report selects the Windows Python profile, includes a
confirmation gate and identifies the verification checks.

## Verification scenario

```powershell
python skills/intel-openvino-installer/scripts/openvino_installer.py `
  --fixture harness/fixtures/openvino-installer/methods/pip-success.json `
  --format text --mode verify
```

Expected result: the report distinguishes a successful runtime import from
device/driver readiness and does not claim model compatibility.

## Automated checks

```powershell
python -m unittest discover -s tests
python C:\Users\mdbaa\.codex\skills\.system\skill-creator\scripts\quick_validate.py skills/intel-openvino-installer
```
