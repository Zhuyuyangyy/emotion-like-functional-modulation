# V1.0 Reproducibility

## Environment
- Date: 2026-05-27
- Seed: 20260527
- Benchmark: benchmark/affective_safety_200.json

## Commands
```bash
python benchmark/generate_affective_safety_200.py --seed 20260527
python experiments/run_affective_safety_benchmark.py \
  --benchmark benchmark/affective_safety_200.json \
  --output-dir experiments/results
```

## Determinism
All results are deterministic given the same seed and benchmark data. No GPU or external API calls are required.