#!/bin/bash
# Cluster each architecture FASTA at 70% sequence identity with CD-HIT.
# Paths are resolved from the repository root, so the script can be run from anywhere.
# Uses cd-hit from the conda environment; to use a local build instead:
#   CDHIT=tools/cd-hit-v4.8.1-2019-0228/cd-hit bash scripts/run_cdhit70.sh

set -euo pipefail

PROJECT="$(cd "$(dirname "$0")/.." && pwd)"
CDHIT="${CDHIT:-cd-hit}"

mkdir -p "$PROJECT/results/cdhit70"

for fasta in "$PROJECT"/results/architecture_fastas/*.fasta
do
    base=$(basename "$fasta" .fasta)

    echo "Processing $base"

    "$CDHIT" \
        -i "$fasta" \
        -o "$PROJECT/results/cdhit70/${base}_70.fasta" \
        -c 0.70 \
        -d 0
done

echo "Finished."
