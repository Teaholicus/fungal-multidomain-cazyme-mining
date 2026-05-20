#!/bin/bash

mkdir -p ../results/dbcan_hits

DBCAN_DB="../tools/dbcan/dbCAN-HMMdb-V14.txt"

for species_dir in ../results/signalp_fast_slow/*; do

    species=$(basename "$species_dir")

    echo "======================================="
    echo "$(date) Processing: $species"
    echo "======================================="

    fasta="$species_dir/validated_secretome.fasta"

    output_dir="../results/dbcan_hits/$species"

    mkdir -p "$output_dir"

    output_file="$output_dir/dbcan_hits.txt"

    # skip completed runs
    if [ -s "$output_file" ]; then
        echo "Skipping completed"
        continue
    fi

    hmmscan \
        --domtblout "$output_file" \
        --cpu 8 \
        "$DBCAN_DB" \
        "$fasta" \
        > /dev/null

done