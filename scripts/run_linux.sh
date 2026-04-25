#!/usr/bin/env bash
set -euo pipefail

SIZE="${1:-100000000}"
RUNS="${2:-30}"
THREADS="${3:-}"

make check-env
make all
mkdir -p results

if [[ -n "$THREADS" ]]; then
  ./build/vector_sum_benchmark --size "$SIZE" --runs "$RUNS" --threads "$THREADS" --output results/raw_times.csv
else
  ./build/vector_sum_benchmark --size "$SIZE" --runs "$RUNS" --output results/raw_times.csv
fi

python3 scripts/analyze.py results/raw_times.csv --out results
