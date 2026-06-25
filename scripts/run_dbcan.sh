#!/bin/bash

mkdir -p ../results/dbcan_hits

DBCAN_DB="../tools/dbcan/dbCAN-HMMdb-V14.txt"

INPUT_FASTA="../results/deeptmhmm/validated_secretome.fasta"

OUTPUT_FILE="../results/dbcan_hits/dbcan_hits.txt"

echo "======================================="
echo "$(date) Running dbCAN HMM scan"
echo "======================================="

echo "Input FASTA:"
echo "$INPUT_FASTA"

echo "Output:"
echo "$OUTPUT_FILE"

hmmscan \
    --domtblout "$OUTPUT_FILE" \
    --cpu 8 \
    "$DBCAN_DB" \
    "$INPUT_FASTA" \
    > ../results/dbcan_hits/hmmscan.log

echo "Done"