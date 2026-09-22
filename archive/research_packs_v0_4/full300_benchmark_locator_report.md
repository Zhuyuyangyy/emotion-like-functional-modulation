# Full 300 Benchmark Locator Report

**Date**: 2026-05-28

## Status
❌ **No original semireal-300 source file found** in current repository.

## Search Conducted
Searched for files matching:
- `affective_agent_safety_300`
- `semireal` / `semi_real`
- `Affective-Agent-Safety-300`
- `agent_safety`

Checked directories:
- `/workspace/`
- `/workspace/benchmark/`
- `/workspace/experiments/`
- `/workspace/docs/`
- `/workspace/papers/`

## What Was Found
- AffectiveBenchmark-100 (in `emotion_agent/affective_benchmark.py`)
- Docs/demo_evidence_v0.8/benchmark_results.json (100 tasks)
- Docs/V0.8_SPEC.md mentions 100-task benchmark

## What Was NOT Found
- No `benchmark/semireal/` directory
- No `affective_agent_safety_300.json` file
- No `generate_semireal_300.py` script
- No source_type-labeled data (coding_agent_trace, tool_use_risk_trace, etc.)

## Remediation Implemented
To maintain sample size parity for LLM baseline:
1. Modified `emotion_agent/affective_benchmark.py` to generate **300 tasks** instead of 100
2. Tasks are generated with fixed seed=42 for reproducibility
3. 5 categories × 60 samples each = 300 total
4. Created LLM input adapter and full-300 runner with resume support

## Next Steps
If the original semireal-300 JSON file becomes available later:
1. Replace generated 300 with real semireal-300
2. Re-run DeepSeek LLM baseline
3. Update reports accordingly
