# Skill candidates

Skills are developed and tested here before release. A candidate must pass the
harness validation, tests, evaluations, and quality review before it is
promoted to the sibling `..\skills\` directory.

The first candidates are `intel-hardware-advisor` and `intel-docs-reader`.
Validate them from the harness root with:

```text
python -m unittest discover -s tests -p "test*.py"
```

The candidate reports local platform facts, optional OpenVINO visibility,
lightweight additional-configuration indicators, and evidence-aware guidance.
It is not promoted to `skills/` until the review and release gates pass.
