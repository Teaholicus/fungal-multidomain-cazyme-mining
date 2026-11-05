# Comparative Genome Mining of Multidomain Fungal CAZymes

A reproducible pipeline that mines the predicted secretomes of 29 fungi for multidomain carbohydrate-active enzymes (CAZymes) and reduces them to a compact, non-redundant set of candidates for enzyme discovery and engineering.

## At a glance

| Analysis stage | Proteins remaining |
|----------------|------------------:|
| Complete fungal proteomes (29 species) | 336,213 |
| SignalP 6 Fast predictions | 24,258 |
| SignalP 6 Slow-sequential validation | 23,417 |
| DeepTMHMM-filtered secretome | 19,631 |
| Secreted CAZyme proteins (dbCAN) | 5,971 |
| Multidomain CAZymes | 312 |
| Non-redundant representative candidates | **191** |

**Key findings**

- The two most abundant multidomain architectures, GH72 + CBM43 and GH71 + CBM24 (82 of 312 proteins), remodel the fungus's *own* cell wall rather than plant biomass.
- Plant cell-wall architectures are more diverse (24 of 47 architectures) but each is individually rarer.
- Cellulose-active multidomain enzymes form a small, well-defined set: 12 representatives in 6 architectures, all GH5, GH7, GH45 or AA9 joined to a CBM.
- One candidate from this set, the GH54 + CBM42 α-L-arabinofuranosidase AbfB from *Aspergillus clavatus*, is taken forward in [rational-enzyme-engineering](https://github.com/Teaholicus/rational-enzyme-engineering).

---

## Why multidomain CAZymes

Industrial biomass conversion relies heavily on secreted fungal CAZymes: cellulases, hemicellulases and oxidative accessory enzymes that deconstruct plant cell walls. Many of the most useful ones combine a catalytic domain with one or more carbohydrate-binding modules (CBMs), which improve substrate targeting, processivity and activity on insoluble substrates.

Genome mining across diverse fungi remains a practical way to find:

- new variants of known enzyme classes
- unusual domain combinations
- candidates from thermophilic species with potentially higher stability
- starting points for protein engineering

The pipeline:

1. collects fungal reference proteomes automatically from UniProt
2. predicts secreted proteins with SignalP 6
3. removes membrane-associated proteins with DeepTMHMM
4. annotates CAZyme domains with HMMER and dbCAN
5. reconstructs multidomain architectures
6. clusters sequences within each architecture and selects representatives
7. sorts representatives into subsets for different downstream questions

The emphasis is on biologically interpretable, traceable results rather than black-box predictions.

---

## Species

29 species were selected for known cellulolytic capability, industrial enzyme production, ecological diversity, thermophilic adaptation and coverage of the major filamentous fungal groups:

- *Trichoderma* (4 species), *Aspergillus* (8), *Penicillium* (4), *Talaromyces* (2), *Fusarium* (2)
- *Neurospora crassa*, *Podospora anserina*, *Chaetomium globosum*, *Pleurotus ostreatus*, *Rhizopus oryzae*, *Yarrowia lipolytica*
- thermophiles: *Myceliophthora thermophila* (syn. *Thermothelomyces thermophilus*), *Thielavia terrestris*, *Chaetomium thermophilum*

Mesophiles and thermophiles were combined to increase the chance of finding unusual architectures and potentially thermostable candidates.

---

## Methods

### 1. Proteome retrieval

Reference proteomes were retrieved through the UniProt REST API. Reference proteomes were preferred, viral entries filtered out, and proteomes with implausible protein counts rejected; taxonomy-based retrieval served as a fallback. The step writes one FASTA file per species and a metadata report.

### 2. Two-stage SignalP 6 secretome prediction

Running the SignalP 6 `slow-sequential` model on all 29 proteomes would take about a week on a desktop workstation. A two-stage workflow was therefore used:

1. **Fast screening** of complete proteomes with the SignalP 6 Fast model
2. **Slow validation** of Fast-positive proteins with `slow-sequential`

The approach was benchmarked against a full `slow-sequential` run on the *Trichoderma reesei* proteome. The two models disagreed on ~0.7% of all proteins and ~9% of secretome-related predictions (Fast-only plus Slow-only calls). Slow validation removed ~3.6% of Fast-positive *T. reesei* proteins, within that expected disagreement range.

Across all 29 species, Slow validation retained 96.4% of Fast-positive proteins on average (range 95.4–98.1%). The hybrid workflow reduced total runtime about 4.3-fold; Fast mode alone is about 6× faster than `slow-sequential`.

The conclusion is that SignalP Fast performs very well for fungal secretome screening, and Slow validation mainly removes marginal predictions.

### 3. DeepTMHMM filtering

Many membrane proteins also carry an N-terminal signal peptide, so a SignalP-positive protein is not necessarily secreted. All 23,417 SignalP-validated proteins were therefore analysed with DeepTMHMM, and only the **SP** class (signal peptide, no transmembrane helices) was kept:

| DeepTMHMM class | Proteins | Action |
|---|---:|---|
| SP | 19,631 | retained |
| SP+TM | 3,192 | removed |
| GLOB (no signal peptide called) | 391 | removed |
| TM | 203 | removed |

DeepTMHMM removed 3,786 proteins (16.2%). Together with Slow validation, the initial SignalP-positive set was reduced by ~19%.

### 4. CAZyme annotation

The filtered secretome was scanned with HMMER3 (`hmmscan`) against the dbCAN HMM database v14. Annotating only after secretome filtering avoids false-positive "secreted" CAZymes that are really intracellular or membrane-bound.

The 59,372 raw HMM matches (across 7,449 proteins) included overlapping, partial and redundant hits. They were filtered in four steps:

| Stage | Domain hits |
|---|---:|
| Raw HMM matches | 59,372 |
| E-value < 1×10⁻¹⁵ and HMM coverage ≥ 35% | 17,662 |
| Overlap filtering | 6,363 |
| Merging of adjacent hits from the same family | 6,315 |

The final 6,315 domain assignments cover 5,971 unique secreted proteins.

### 5. Architecture reconstruction

Filtered domains were assembled, in sequence order, into one architecture per protein.

| Metric | Value |
|---|---:|
| CAZyme proteins | 5,971 |
| Multidomain proteins | 312 |
| Distinct multidomain architectures | 55 |
| Distinct architectures, excluding pure repeats of one domain | 47 |

Architectures made only of repeated copies of one domain were excluded, to focus on combinations of different functional modules.

### 6. Clustering within architectures

Proteins were clustered separately within each architecture using CD-HIT at 70% sequence identity. Clustering within, not across, architectures avoids merging proteins with different domain organisations. The 70% threshold collapses near-identical orthologs while keeping potentially distinct functional variants. One representative was kept per cluster, with links to all cluster members.

### 7. Candidate subsets

Representatives were annotated with a functional group, assigned from their CAZyme families by exact family match (subfamily numbers ignored), and flagged as conserved, thermophile-derived, Swiss-Prot reviewed, or rare.

---

## Results

### Secretome size across species

Proteomes ranged from 6,454 to 15,531 proteins. SignalP-validated secretomes made up 3.9–9.5% of each proteome (mean 7.2%). After DeepTMHMM filtering the final secretome was 3.2–8.2% (mean 6.0%), with DeepTMHMM retaining 77–90% of SignalP-validated proteins per species.

*Podospora anserina* and *Pleurotus ostreatus* had the largest final secretome fractions; *Rhizopus oryzae* had the smallest. These differences likely reflect ecological specialisation and different strategies for extracellular biomass degradation.

| Species | Proteome | SignalP Fast | SignalP Slow | DeepTMHMM final | Final secretome | DeepTMHMM retention |
|---|---:|---:|---:|---:|---:|---:|
| *Fusarium graminearum* | 14,147 | 1,298 | 1,259 | 1,075 | 7.60% | 85.39% |
| *Chaetomium globosum* | 11,038 | 1,009 | 974 | 808 | 7.32% | 82.96% |
| *Aspergillus niger* | 14,069 | 955 | 913 | 765 | 5.44% | 83.79% |
| *Trichoderma reesei* | 9,115 | 666 | 642 | 535 | 5.87% | 83.33% |
| *Penicillium oxalicum* | 9,977 | 660 | 630 | 515 | 5.16% | 81.75% |

![Secretome fraction across species](results/figures/secretome_fraction_across_species.png)

### Most common multidomain architectures

| Architecture | Proteins | Species | Typical function |
|---|---:|---:|---|
| GH72 + CBM43 | 48 | 23 | β-1,3-glucanosyltransferase; fungal cell wall |
| GH71 + CBM24 | 34 | 19 | α-1,3-glucanase; fungal cell wall |
| GH15 + CBM20 | 30 | 20 | glucoamylase; starch |
| GH54 + CBM42 | 28 | 19 | α-L-arabinofuranosidase; hemicellulose |
| AA8 + AA3_1 | 27 | 15 | cellobiose dehydrogenase; oxidative cellulose degradation |
| GH43_14 + CBM91 | 19 | 14 | GH43 hemicellulase |
| GH13_1 + CBM20 | 16 | 14 | α-amylase; starch |
| GH43_36 + CBM91 | 13 | 9 | GH43 hemicellulase |

The two most abundant architectures act on the fungal cell wall, not on plant biomass. GH72 enzymes are typically GPI-anchored at the cell surface. Because DeepTMHMM does not predict GPI anchors, some of these proteins are probably cell-surface-bound rather than truly secreted (see Limitations).

The classic plant-biomass architectures are much less abundant: GH7 + CBM1 (cellobiohydrolase) occurs in 11 proteins from 7 species, and GH10 + CBM1 (xylanase) in 6 proteins from 6 species.

![Most common multidomain architectures](results/figures/multidomain_architecture_frequency.png)

### Distribution across species

Some architectures recur within a few species, while others are conserved across diverse lineages. To separate abundance from evolutionary distribution, architectures were also ranked by the number of species in which they occur.

![Architecture distribution across species](results/figures/multidomain_architecture_species_distribution.png)

The overall landscape shows a small number of widely conserved architectures alongside many rare ones.

![Architecture landscape](results/figures/multidomain_architecture_landscape.png)

### Thermophilic fungi

Most multidomain architectures found in the three thermophiles also occur in mesophiles. This suggests that thermal adaptation acts mainly at the sequence level rather than through unique domain combinations.

### Protein length within architectures

Most architectures have fairly uniform protein lengths, but several vary widely because of long linkers or additional accessory regions:

- **GH71 + CBM24**: about 570 to 1,740 amino acids
- **GH18 + CBM24**: secreted chitinases exceeding 2,000 amino acids

![Architecture lengths](results/figures/multidomain_CAZyme_architectures.png)

### Sequence diversity and conservation

Clustering produced **191 representatives** from **47 architectures**, covering **all 29 species**. Some architectures form a few large clusters, while others fragment into many small groups despite sharing identical domain organisation.

![Sequence diversity](results/figures/Sequence_diversity_of_multidomain_architectures.png)

Cluster membership often follows fungal phylogeny. GH72 + CBM43 and GH71 + CBM24, for example, each contain several conserved sequence groups that recur across independent lineages, consistent with conserved function plus lineage-specific diversification.

GH72 + CBM43

![GH72](results/figures/gh72__CBM43_cluster_presence.png)

GH71 + CBM24

![GH71](results/figures/GH71_CBM24_cluster_presence.png)

### Candidate subsets

**By functional group** (assigned from CAZyme families):

| Functional group | Architectures | Proteins | Representatives |
|---|---:|---:|---:|
| Cellulose (GH5, GH6, GH7, GH12, GH45, AA9) | 6 | 23 | 12 |
| Hemicellulose (e.g. GH10, GH11, GH43, GH54, GH74) | 14 | 94 | 50 |
| Pectin (e.g. GH28, GH78, GH93, CE8) | 4 | 7 | 5 |
| Oxidative auxiliary activities (AA) | 4 | 34 | 19 |
| Fungal cell wall & chitin (GH16, GH18, GH71, GH72, GH76) | 9 | 93 | 62 |
| Starch, fructan & other | 10 | 61 | 43 |
| **Total** | **47** | **312** | **191** |

The three plant cell-wall groups together give **67 representatives** in 24 architectures.

**By selection criterion** (these overlap with each other and with the functional groups):

| Subset | Representatives |
|---|---:|
| Conserved (cluster spans ≥ 3 species) | 27 |
| Rare (architecture found in a single protein) | 22 |
| Thermophile-derived | 18 |
| Swiss-Prot reviewed | 7 |

These subsets let a user prioritise candidates for a given question without rerunning the pipeline.

![Candidate subsets](results/figures/candidate_subsets.png)

### Representative cluster coverage

Each representative stands for a homologous sequence group. In the plot below, architectures near the upper right are dominated by a single conserved group; those near the lower left contain many distinct groups and are therefore richer sources of sequence diversity.

![Representative coverage](results/figures/cluster_coverage.png)

---

## Pipeline outputs

| File (`results/tables/`) | Description |
|------|-------------|
| `representative_candidates.csv` | All 191 non-redundant representatives, with functional group and flags |
| `cluster_members.csv` | Mapping between representatives and cluster members |
| `architecture_summary.csv` | Architecture-level statistics |
| `architecture_fasta_summary.csv` | FASTA datasets used for clustering |
| `plant_cell_wall_candidates.csv` | Cellulose, hemicellulose and pectin representatives |
| `cellulase_candidates.csv` | Cellulose-active representatives |
| `conserved_candidates.csv` | Representatives of clusters spanning ≥ 3 species |
| `thermophile_candidates.csv` | Representatives from thermophilic fungi |
| `reviewed_candidates.csv` | Swiss-Prot reviewed representatives |
| `rare_architectures.csv` | Representatives of single-protein architectures |

---

## How to run

### Requirements

```bash
conda env create -f environment.yml
conda activate enzyme_mining
```

The environment provides Python, Biopython, pandas, plotting libraries, HMMER and CD-HIT. Three components cannot be redistributed and are installed separately:

- **SignalP 6.0** (academic licence from DTU Health Tech), installed into the same environment. The `slow-sequential` model weights are expected in `tools/signalp6_slow_sequential/models/`.
- **DeepTMHMM 1.0**, run through the DTU web service or BioLib rather than locally.
- **dbCAN HMM database v14** (`dbCAN-HMMdb-V14.txt`) in `tools/dbcan/`, indexed once with `hmmpress tools/dbcan/dbCAN-HMMdb-V14.txt`.

`data/proteomes/` and `tools/` are not tracked in git, because of their size and licences. Scripts use paths relative to `scripts/`, and notebooks relative to `notebooks/`, so run each from its own folder. The project was developed under WSL / Ubuntu.

### Running order

| # | Step | Produces |
|---|------|----------|
| 1 | `notebooks/1_Proteomes_loader.ipynb` | `data/proteomes/*.fasta`, `reference_proteomes_report.csv` |
| 2 | `scripts/run_signalp_fast.py` | SignalP Fast predictions per species, `results/signalp_fast/` |
| 3 | `scripts/run_signalp_fast_slow.py` | Slow-sequential validation of Fast-positive proteins, `results/signalp_fast_slow/` |
| 4 | `notebooks/2_SignalP_predictions_prep.ipynb` | Combined `all_signalp_predictions.fasta` and `protein_species_map.csv` |
| 5 | DeepTMHMM (external) on `all_signalp_predictions.fasta` | Unpacked output in `results/deeptmhmm/full_run/` |
| 6 | `notebooks/4_DeepTMHMM_filter.ipynb` | `validated_secretome.fasta`, DeepTMHMM classification tables |
| 7 | `notebooks/3_Proteome statistics.ipynb` | Per-species secretome statistics and figures (needs step 6) |
| 8 | `scripts/run_dbcan.sh` | `results/dbcan_hits/dbcan_hits.txt` |
| 9 | `notebooks/5_CAZymes_parser.ipynb` | Filtered domains, architectures, `candidate_proteins.csv` |
| 10 | `notebooks/6_Clustering_data_prep.ipynb` | One FASTA per architecture, `results/architecture_fastas/` |
| 11 | `scripts/run_cdhit70.sh` | CD-HIT clusters at 70% identity, `results/cdhit70/` |
| 12 | `notebooks/7_Parse_Clusters.ipynb` | Cluster statistics, `architecture_representatives.csv`, `cluster_members.csv` |
| 13 | `notebooks/8_Final_Candidate_Selection.ipynb` | Candidate subsets and summary figures |

---

## Limitations

- **GPI-anchored proteins are not filtered.** DeepTMHMM detects transmembrane helices, not GPI anchors, so some predicted "secreted" proteins (notably GH72 family members) are probably attached to the cell surface. Adding NetGPI is the obvious next filter.
- **Domains are called by HMMER alone.** The standard dbCAN workflow also uses DIAMOND and dbCAN-sub and takes a consensus. Strict E-value and coverage thresholds compensate partly, but borderline domains may be missed or mis-assigned.
- **Functional groups are inferred from family membership.** Several CAZyme families contain more than one activity, so a family label is a hypothesis about function, not a measurement.
- **Predicted secretomes, not expressed ones.** The pipeline reports what a genome can secrete, not what is produced under industrial conditions.

---

## Outlook

- NetGPI filtering of the secretome
- AlphaFold models for representatives
- identification of catalytic residues and substrate-binding sites (implemented for one candidate in [rational-enzyme-engineering](https://github.com/Teaholicus/rational-enzyme-engineering))
- prediction of thermostability
- protein language model embeddings for sequence comparison
- automated comparison against experimentally characterised CAZymes
- novelty assessment against patent sequence databases
- extension to newly sequenced fungal genomes and other microbial taxa

Because each stage is modular, these can be added without restructuring the workflow.

---

## A note on authorship

The pipeline design, the choice of methods, and the interpretation of the results are mine. An LLM was used as a coding and writing assistant throughout, most visibly in code annotation and other documentation.

---

## References

- **SignalP 6.0:** Teufel F, et al. (2022) *Nat Biotechnol* 40:1023–1025. [doi:10.1038/s41587-021-01156-3](https://www.nature.com/articles/s41587-021-01156-3)
- **DeepTMHMM:** Hallgren J, et al. (2022) *bioRxiv*. [doi:10.1101/2022.04.08.487609](https://doi.org/10.1101/2022.04.08.487609)
- **dbCAN3:** Zheng J, et al. (2023) *Nucleic Acids Res* 51(W1):W115–W121. [Article](https://academic.oup.com/nar/article/51/W1/W115/7147496). HMM database v14: [dbCAN2 downloads](https://pro.unl.edu/dbCAN2/browse_download.php)
- **CD-HIT 4.8.1:** Fu L, et al. (2012) *Bioinformatics* 28:3150–3152. [doi:10.1093/bioinformatics/bts565](https://academic.oup.com/bioinformatics/article/28/23/3150/192160)
- **HMMER:** Eddy SR (2011) *PLoS Comput Biol* 7:e1002195. [doi:10.1371/journal.pcbi.1002195](https://doi.org/10.1371/journal.pcbi.1002195)
