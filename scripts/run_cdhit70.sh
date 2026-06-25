#!/bin/bash

PROJECT=/mnt/n/Jupiter_Projects/mining-multidomain-cellulases

mkdir -p "$PROJECT/results/cdhit70"

cd "$PROJECT/tools/cd-hit-v4.8.1-2019-0228"

for fasta in "$PROJECT"/results/architecture_fastas/*.fasta
do
    base=$(basename "$fasta" .fasta)

    echo "Processing $base"

    ./cd-hit \
        -i "$fasta" \
        -o "$PROJECT/results/cdhit70/${base}_70.fasta" \
        -c 0.70 \
        -d 0
done

echo "Finished."
