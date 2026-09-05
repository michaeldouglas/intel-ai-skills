# Quickstart: Runtime Skills Suite

Each skill must first be asked to create a plan. A user then confirms only the
specific mutation they want.

## Convert

```text
Prepare my ONNX model for OpenVINO, show the conversion plan and output files,
but do not write anything until I confirm.
```

## Run

```text
Run this OpenVINO model in the test workspace using Docker and report the
available and effective devices. Start with a plan only.
```

## Benchmark

```text
Benchmark this model on CPU and AUTO with a reproducible configuration. Do not
make a recommendation until the measurements and limitations are shown.
```

## Optimize

```text
Plan post-training quantization for this model, preserving the original files
and requiring accuracy validation before replacing anything.
```

## Serve

```text
Prepare a local OpenVINO Model Server Docker test using ./teste as the model
workspace. Show image, volumes, ports, and health checks before starting it.
```

## GenAI

```text
Plan a documented OpenVINO GenAI test for this model and device. Show package,
model, NPU, and metric prerequisites before downloading or running anything.
```
