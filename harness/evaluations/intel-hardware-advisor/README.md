# Intel Hardware Advisor Evaluation

The scenario file defines the release expectations for the first skill. Run
the deterministic suite from the harness root:

```text
python -m unittest discover -s tests -p "test*.py"
```

The supported-platform scenarios may return qualified guidance, but the
recommendation must retain evidence IDs and guardrails. Missing, conflicting,
unsupported, and permission-failure scenarios must preserve facts and return
an explicit no-decision or failure-aware result. No scenario authorizes claims
about benchmarks, model compatibility, precision, or memory savings.

Physical hardware and network access are not part of this evaluation.
