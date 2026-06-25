# Project Journal

## Project Overview

This journal contains implementation notes, troubleshooting steps, installation instructions, and workflow details that are intentionally omitted from the main README.

The goal is reproducibility and future maintenance rather than portfolio presentation.

---

# Proteome Collection

## Source

Proteomes were downloaded from UniProt.

Reference proteomes were preferred whenever available.

Reference proteome search:

```python
https://rest.uniprot.org/proteomes/search
```

Download:

```python
https://rest.uniprot.org/uniprotkb/stream?format=fasta&query=(proteome:PROTEOME_ID)
```

---

## Reference Proteome Selection Logic

For each species:

1. Query UniProt Proteomes.
2. Keep only reference proteomes.
3. Remove viral entries.
4. Prefer proteomes between 8,000 and 20,000 proteins.
5. Select the largest candidate within that range.

Reasoning:

* Smaller proteomes are often incomplete.
* Very large proteomes frequently represent assembly artifacts or duplicated gene models.

---

## Fallback Proteome Logic

Some species do not have a UniProt reference proteome.

Fallback procedure:

1. Search UniProt Taxonomy.
2. Retrieve candidate taxonomic IDs.
3. Download proteins for each taxon:

```python
organism_id:TAX_ID
```

4. Remove viral entries.
5. Keep candidates with >3000 proteins.
6. Select the largest candidate.

Important:

Fallback species must be manually checked.

A discovered issue:

### Penicillium funiculosum

Taxonomy search returned:

```text
128442  Talaromyces pinophilus
28572   Talaromyces funiculosus
```

The fallback algorithm selected tax_id 128442 because it contained >11,000 proteins.

This corresponded to Talaromyces pinophilus rather than Talaromyces funiculosus.

Result:

* Proteome removed from the study.
* No SignalP or dbCAN reruns were required.
* Downstream analyses were regenerated after removing the species.

Lesson learned:

Store selected tax_id in the proteome report and manually validate fallback species.

---

# SignalP 6

## Environment

Conda environment:

```bash
signalpf_env
```

---

## Fast Prediction

Tool:

```text
tools/signalp6_fast
```

Input:

```text
data/proteomes/*.fasta
```

Output:

```text
results/signalp_fast/
```

Processing time:

~28 hours for 30 fungal proteomes.

---

## Slow Sequential Validation

Tool:

```text
tools/signalp6_slow_sequential
```

Input:

Fast-predicted secretome.

Output:

```text
results/signalp_fast_slow/
```

Processing time:

~10 hours.

---

## Validation Strategy

Full slow-sequential prediction for all proteomes would require approximately one week of continuous runtime.

Compromise:

```text
Proteome
↓
SignalP Fast
↓
Candidate Secretome
↓
SignalP Slow Sequential
↓
DeepTMHMM
↓
Validated Secretome
```
DeepTMHMM in Ubuntu shell example:
time python predict.py \
    --fasta /mnt/n/Jupiter_Projects/mining-multidomain-cellulases/results/signalp_fast_slow/all_signalp_predictions.fasta \
    --output-dir /mnt/n/Jupiter_Projects/mining-multidomain-cellulases/results/deeptmhmm/full_run


Validation against Trichoderma reesei:

* Fast vs Slow disagreement ~9% within the predicted secretome.
* Fast→Slow filtering removed ~3.6% of secreted proteins.
* Across all species retention averaged ~96.5%.

Result:

Fast→Slow validation provided a substantial speed improvement while preserving almost all secretome predictions.

---

## Important SignalP Pitfall

SignalP produces:

```text
prediction_results.txt
processed_entries.fasta
```

processed_entries.fasta contains proteins after signal peptide removal.

These sequences must NOT be used as input for the second SignalP pass.

Correct workflow:

1. Extract IDs predicted as SP.
2. Recover full-length proteins from the original proteome.
3. Run Slow SignalP on full-length proteins.

Using processed proteins effectively tests whether a protein contains a second signal peptide.

---


## dbCAN HMM Scan

Purpose:
Identify CAZyme domains in the DeepTMHMM-filtered fungal secretome using the dbCAN HMM database.

Environment:

```bash
conda activate enzyme_mining
```

Run from Ubuntu / WSL:

```bash
cd /mnt/n/Jupiter_Projects/mining-multidomain-cellulases/scripts

bash run_dbcan.sh
```

Script location:

```text
scripts/run_dbcan.sh
```

Input:

```text
results/deeptmhmm/validated_secretome.fasta
```

Database:

```text
tools/dbcan/dbCAN-HMMdb-V14.txt
```

Output:

```text
results/dbcan_hits/dbcan_hits.txt
results/dbcan_hits/hmmscan.log
```

Command executed by script:

```bash
hmmscan \
    --domtblout results/dbcan_hits/dbcan_hits.txt \
    --cpu 8 \
    tools/dbcan/dbCAN-HMMdb-V14.txt \
    results/deeptmhmm/validated_secretome.fasta
```

Notes:

* Original pipeline ran one hmmscan job per species.
* After introducing DeepTMHMM filtering, all validated secreted proteins are combined into a single FASTA file.
* A single dbCAN scan is performed against the entire validated secretome.
* Species information is preserved through protein identifiers and mapping tables generated in downstream notebooks.
* The CAZyme parser notebook must be updated to read a single `dbcan_hits.txt` file instead of iterating over species folders.


---

## Filtering Strategy

Raw dbCAN predictions contain many overlapping domain calls.

Filtering:

```python
E-value < 1e-15
coverage >= 0.35
```

Then:

1. Remove overlapping domains.
2. Merge neighboring hits belonging to the same family.

Purpose:

Generate clean domain architectures for downstream analysis.

---

# CAZyme Architecture Analysis

Definitions:

```text
Protein
↓
One or more CAZyme domains
↓
Domain Architecture
```

Example:

```text
GH7 + CBM1
```

---

## Architecture Categories

All multidomain architectures:

```text
architecture_summary.csv
```

Biomass-focused subset:

```text
biomass_architectures.csv
```

Generated by filtering architectures containing:

```text
GH5
GH6
GH7
GH10
GH11
GH12
GH45
AA9
```

Used for cellulase-oriented exploration.

Later analyses returned to the complete architecture dataset.

---

# WSL Setup

Several bioinformatics tools were easier to install under Linux than Windows.

Used:

```text
Windows Subsystem for Linux (Ubuntu)
```

---

## Useful Commands

Check current user:

```bash
whoami
```

Update repositories:

```bash
sudo apt update
```

Install compiler:

```bash
sudo apt install g++
```

Install make:

```bash
sudo apt install make
```

Install zlib development headers:

```bash
sudo apt install zlib1g-dev
```

---

## Common Issue

Error:

```text
fatal error: zlib.h: No such file or directory
```

Solution:

```bash
sudo apt install zlib1g-dev
```

---

# CD-HIT Installation

Downloaded source:

```text
cd-hit-v4.8.1-2019-0228.tar.gz
```

Unpack:

```bash
tar -xzf cd-hit-v4.8.1-2019-0228.tar.gz
```

Compile:

```bash
cd cd-hit-v4.8.1-2019-0228
make
```

Executable:

```text
cd-hit
```

---

# CD-HIT Clustering

Run from Ubuntu shell.

Directory:

```text
tools/cd-hit-v4.8.1-2019-0228
```

Run script:
bash /mnt/n/Jupiter_Projects/mining-multidomain-cellulases/scripts/run_cdhit70.sh
```

---

## Interpretation

CD-HIT clusters proteins sharing ≥70% sequence identity.

Example:

```text
GH72 + CBM43
49 proteins
22 clusters
```

Meaning:

The architecture is widespread but sequence-diverse.

Clusters are later used to select representative proteins for deeper characterization.

---

